#!/usr/bin/env python
# encoding: utf-8

"""
@author: thsheep
@file: scheduler.py
@time: 2018/2/4 02:00
@site:
"""

import time
import json
import logging
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from apscheduler.executors.pool import ThreadPoolExecutor

from gerapy.server.core.utils import get_scrapyd
from gerapy.server.core.models import Task, Client

logger = logging.getLogger(__name__)

db_time_format = "%Y-%m-%d %H:%M:%S"

executors = {
    'default': ThreadPoolExecutor(20)
}
scheduler = BackgroundScheduler(executors=executors)
scheduler.add_jobstore(DjangoJobStore(), "default")


def work_func(client, project, spider):
    ip_port = Client.objects.get(id=client)
    scrapyd = get_scrapyd(ip_port)
    logger.warning("Run {}: {} on server{}".format(project, spider, ip_port.ip))
    try:
        jobs = scrapyd.schedule(project, spider)
        logger.warning("{}:  {}；Jobs：{}".format(project, spider, jobs))
    except Exception as err:
        logger.error("Please deploy the project to：{}".format(ip_port.ip))


class CreateSchedulerWork(threading.Thread):
    def __init__(self, scheduler):
        super(CreateSchedulerWork, self).__init__()
        self.scheduler = scheduler
        self.setDaemon(True)
    
    def run(self):
        logger.warning("CreateSchedulerWork")
        while True:
            try:
                tmp = []
                scheduler_jobs_ids = [_id.id for _id in self.scheduler.get_jobs()]
                task_model = Task.objects.all()
                for task in task_model:
                    if task.success == 0:
                        configuration = json.loads(task.configuration)
                        configuration = {key: value for key, value in configuration.items() if value}
                        for client in json.loads(task.clients):
                            job_id = "%s-%s" % (task.id, client)
                            configuration.update({'id': job_id})
                            tmp.append(job_id)
                            if job_id not in scheduler_jobs_ids:
                                if Client.objects.filter(pk=client):
                                    logger.warning("Create a scheduled task：{}: {}".format(task.project,
                                                                                           task.spider))
                                    self.scheduler.add_job(work_func,
                                                           task.trigger,
                                                           **configuration,
                                                           args=[client, task.project, task.spider])
                        Task.objects.filter(id=task.id).update(success=1)
                    
                    scheduler_jobs_ids = [_id.id for _id in self.scheduler.get_jobs()]
                    client_ids = Client.objects.values_list("id", flat=True)
                    client_difference = [i.split('-')[1] for i in scheduler_jobs_ids]
                    client_difference_set = [i for i in client_difference if int(i) not in client_ids]
                    remove_jobs = [i for i in scheduler_jobs_ids if i.split('-')[1] in client_difference_set]
                    if scheduler_jobs_ids:
                        for i in tmp:
                            if i not in scheduler_jobs_ids:
                                remove_jobs.append(i)
                    # 更新已创建的定时任务
                    if remove_jobs:
                        for jobs in remove_jobs:
                            if jobs in scheduler_jobs_ids:
                                self.scheduler.remove_job(jobs)
                                logger.warning("Delete job ID：{}".format(jobs))
                tmp.clear()
                time.sleep(5)
            except Exception as ex:
                logger.error(str(ex))


register_events(scheduler)
scheduler.start()
logger.info("Scheduler started!")
print("Scheduler started!")
add_work = CreateSchedulerWork(scheduler)
add_work.start()
logger.info("Add_Work started!")
print("Add_Work started!")

#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: thsheep
@file: scheduler.py
@time: 2018/2/4 02:00
@site:
"""
# 　　　┏┓　　　┏┓
# 　　┏┛┻━━━┛┻┓
# 　　┃　　　　　　　 ┃
# 　　┃　　　━　　　 ┃
# 　　┃　┳┛　┗┳　┃
# 　　┃　　　　　　　 ┃
# 　　┃　　　┻　　　 ┃
# 　　┃　　　　　　　 ┃
# 　　┗━┓　　　┏━┛Codes are far away from bugs with the animal protecting
# 　　　　┃　　　┃    神兽保佑,代码无bug
# 　　　　┃　　　┃
# 　　　　┃　　　┗━━━┓
# 　　　　┃　　　　　 ┣┓
# 　　　　┃　　　　 ┏┛
# 　　　　┗┓┓┏━┳┓┏┛
# 　　　　　┃┫┫　┃┫┫
# 　　　　　┗┻┛　┗┻┛
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
    logger.warning(f"开始在服务器：{ip_port.ip} 运行 {project}-{spider}")
    try:
        jobs = scrapyd.schedule(project, spider)
        logger.warning(f"运行{project}-{spider}成功；作业ID为：{jobs}")
    except Exception as err:
        logger.error(f"请先部署项目到：{ip_port.ip}")


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
                client_ids = Client.objects.values_list("id", flat=True)
                client_difference = [i.split('-')[1] for i in scheduler_jobs_ids]
                client_difference_set = [i for i in client_difference if int(i) not in client_ids]
                for task in task_model:
                    if task.success == 0:
                        configuration = json.loads(task.configuration)
                        configuration = {key: value for key, value in configuration.items() if value}
                        if configuration.get('run_time', False):
                            run_date = configuration.pop('run_time')
                            configuration.update({'run_date': run_date})
                        for client in json.loads(task.clients):
                            job_id = f"{task.id}-{client}"
                            configuration.update({'id': job_id})
                            tmp.append(job_id)
                            if job_id not in scheduler_jobs_ids:
                                if Client.objects.filter(pk=client):
                                    logger.warning(f"创建定时任务：{task.project}: {task.spider}")
                                    self.scheduler.add_job(work_func,
                                                           task.trigger,
                                                           **configuration,
                                                           args=[client, task.project, task.spider])
                        Task.objects.filter(id=task.id).update(success=1)
                    #  更新已创建的定时任务
                    remove_jobs = [i for i in scheduler_jobs_ids if i.split('-')[1] in client_difference_set]
                    remove_jobs.extend([i for i in tmp if i not in scheduler_jobs_ids])
                    if remove_jobs:
                        for jobs in remove_jobs:
                            if jobs in scheduler_jobs_ids:
                                self.scheduler.remove_job(jobs)
                                logger.warning(f"删除作业ID：{jobs}")
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
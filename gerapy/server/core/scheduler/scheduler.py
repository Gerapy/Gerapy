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
from scrapyd_api import ScrapydAPI

from gerapy.server.core.utils import scrapyd_url
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
    scrapyd = ScrapydAPI(scrapyd_url(ip_port.ip, ip_port.port))
    scrapyd.schedule(project, spider)


class CreateSchedulerWork(threading.Thread):

    def __init__(self, scheduler):
        super(CreateSchedulerWork, self).__init__()
        self.lock = threading.Lock()
        self.scheduler = scheduler
        self.quit_flag = False
        self.stop_flag = True
        self.setDaemon(True)

    def run(self):
        logger.warning("CreateSchedulerWork")
        while not self.quit_flag:
            self.lock.acquire()
            if self.stop_flag:
                self.lock.release()
                continue
            try:
                task_model = Task.objects.all()
                for task in task_model:
                    if task.success == 0:
                        configuration = json.loads(task.configuration)
                        configuration = {key: value for key, value in configuration.items() if value}
                        if configuration.get('run_time', False):
                            run_date = configuration.pop('run_time')
                            configuration.update({'run_date': run_date})
                        configuration.update({'id': f'{task.id}'})
                        for client in json.loads(task.clients):
                            self.scheduler.add_job(work_func,
                                                   task.trigger,
                                                   **configuration,
                                                   args=[client, task.project, task.spider])
                            Task.objects.filter(id=task.id).update(success=1)
                scheduler_jobs_ids = [_id.id for _id in self.scheduler.get_jobs()]
                task_id = Task
                time.sleep(5)
            except Exception as ex:
                self.lock.release()
                raise RuntimeError("错误格式: %s" % (str(ex)))
            finally:
                self.lock.release()

    def start_add_work(self):
        self.lock.acquire()
        if self.quit_flag:
            self.lock.release()
            return
        self.stop_flag = False
        self.lock.release()


register_events(scheduler)
scheduler.start()
logger.info("Scheduler started!")
print("Scheduler started!")
add_work = CreateSchedulerWork(scheduler)
add_work.start()
add_work.start_add_work()
logger.info("Add_Work started!")
print("Add_Work started!")
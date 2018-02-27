#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23 23:09
# @Author  : thsheep
# @Site    :
# @File    : scheduler_bak.py
# @Software: PyCharm

import time
import logging
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


@scheduler.scheduled_job("interval", seconds=60, id="scheduler_job")
def scheduler_job():
    """
    每分钟检查一次定时任务
    :return:
    """
    models = Task.objects.all()
    for model in models:
        scheduler_at = model.scheduler_at
        updated_at = model.updated_at
        scheduler_at_time_stamp = scheduler_at * 60
        updated_at_time_stamp = time.mktime(updated_at.timetuple())
        if time.time() - updated_at_time_stamp > scheduler_at_time_stamp:
            client_id = model.client_id
            project_name = model.project_name
            spider_name = model.spider_name
            client = Client.objects.get(id=client_id)
            scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
            try:
                job = scrapyd.schedule(project_name, spider_name)
                model.success = 1
            except ConnectionError:
                model.success = 0
            finally:
                model.save()


register_events(scheduler)
scheduler.start()
scheduler.add_job()
logger.info("Scheduler started!")
print("Scheduler started!")
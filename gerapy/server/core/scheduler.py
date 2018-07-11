import time
from threading import Thread
import json
from django_apscheduler.models import DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from gerapy.server.core.models import Client, Task
from gerapy.server.server.settings import SCHEDULER_HEARTBEAT
from gerapy.server.core.utils import get_scrapyd, clients_of_task, get_job_id

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')

# map the args
args_map = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date',
             'timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}


def execute(client, project_name, spider_name):
    """
    schedule deployed task
    :param client: client object
    :param project_name: project name
    :param spider_name: spider name
    :return: None
    """
    print('Execute', 'Client', client.name, 'Project Name',
          project_name, 'Spider Name', spider_name)
    # don not add any try except, apscheduler can catch traceback to database
    ip_port = Client.objects.get(id=client.id)
    scrapyd = get_scrapyd(ip_port)
    scrapyd.schedule(project_name, spider_name)


class SchedulerManager(Thread):
    def __init__(self, scheduler):
        """
        init manager
        :param scheduler:
        """
        super(SchedulerManager, self).__init__()
        self.scheduler = scheduler
        register_events(self.scheduler)
        self.setDaemon(True)
        self.scheduler.start()
    
    def existed_jobs(self):
        """
        get existed jobs stored in db
        :return:
        """
        jobs = DjangoJob.objects.all()
        return jobs
    
    def realtime_tasks(self):
        """
        get real-time tasks from db
        :return:
        """
        tasks = Task.objects.all()
        return tasks
    
    def realtime_jobs(self):
        """
        get real-time jobs
        :return:
        """
        tasks = self.realtime_tasks()
        for task in tasks:
            clients = list(clients_of_task(task))
            for client in clients:
                job_id = get_job_id(client, task)
                yield job_id
    
    def sync_jobs(self):
        """
        sync jobs
        :return:
        """
        # add new jobs or modify existed jobs
        self._add_or_modify_jobs()
        # remove deleted jobs
        self._remove_jobs()
    
    def _remove_jobs(self):
        """
        remove jobs
        :return:
        """
        # get existed ids
        existed_jobs = DjangoJob.objects.values_list('name', flat=True)
        # get real-time ids
        realtime_jobs = list(self.realtime_jobs())
        # get ret ids
        ret_jobs = [i for i in existed_jobs if i not in realtime_jobs]
        # remove job according to ids
        for ret_job in ret_jobs:
            self.scheduler.remove_job(ret_job)
    
    def _add_or_modify_jobs(self):
        """
        add new jobs or modify existed jobs
        :return:
        """
        tasks = self.realtime_tasks()
        for task in tasks:
            # if modified
            if task.modified:
                clients = list(clients_of_task(task))
                # update for every client
                for client in clients:
                    # get job id
                    job_id = get_job_id(client, task)
                    configuration = json.loads(task.configuration)
                    trigger = task.trigger
                    configuration = {arg: configuration.get(arg) for arg in args_map.get(trigger) if
                                     configuration.get(arg)}
                    # if job doesn't exist, add it. otherwise replace it
                    self.scheduler.add_job(execute, task.trigger, args=[client, task.project, task.spider], id=job_id,
                                           replace_existing=True, **configuration)
                task.modified = 0
                task.save()
    
    def run(self):
        """
        heart beat detect
        :return:
        """
        while True:
            self.sync_jobs()
            time.sleep(SCHEDULER_HEARTBEAT)


# init scheduler manager
sm = SchedulerManager(scheduler)
# new thread
sm.start()

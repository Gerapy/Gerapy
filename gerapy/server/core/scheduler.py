import time
from threading import Thread
import json
from django_apscheduler.models import DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from gerapy import get_logger
from gerapy.server.core.models import Client, Task
from gerapy.settings import SCHEDULER_HEARTBEAT
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

logger = get_logger(__name__)


def execute(client, project_name, spider_name):
    """
    schedule deployed task
    :param client: client object
    :param project_name: project name
    :param spider_name: spider name
    :return: None
    """
    logger.info('execute job of client %s, project %s, spider %s',
                client.name, project_name, spider_name)
    # don not add any try except, apscheduler can catch traceback to database
    ip_port = Client.objects.get(id=client.id)
    scrapyd = get_scrapyd(ip_port)
    scrapyd.schedule(project_name, spider_name)


class SchedulerManager(Thread):
    """
    Scheduler of tasks
    """

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

    def sync_jobs(self, force=False):
        """
        sync jobs
        :return:
        """
        logger.debug('syncing jobs from tasks configured...')
        tasks = self.realtime_tasks()
        logger.debug('get realtime tasks %s', tasks)
        for task in tasks:
            # add new jobs or modify existed jobs
            self._add_or_modify_new_jobs(task, force)
            # remove deleted jobs
            self._remove_deprecated_jobs(task, force)

            task.modified = 0
            task.save()

        logger.debug('successfully synced task with jobs')
        if force:
            logger.info('successfully synced task with jobs with force')

    def _remove_deprecated_jobs(self, task, force=False):
        """
        remove jobs
        :return:
        """
        if not task.modified and not force:
            return
        # check extra jobs which does not belong to task
        existed_jobs = self.existed_jobs()
        existed_job_ids = list(map(lambda obj: obj.id, existed_jobs))
        realtime_job_ids = list(self.realtime_jobs())
        logger.debug('existed job ids %s, task job ids %s',
                     existed_job_ids, realtime_job_ids)
        deprecated_job_ids = [
            job_id for job_id in existed_job_ids if not job_id in realtime_job_ids]
        if deprecated_job_ids:
            logger.info('deleting deprecated jobs')
            # remove deprecated jobs
            for job_id in deprecated_job_ids:
                self.scheduler.remove_job(job_id)
            logger.info('deleted deprecated jobs %s', deprecated_job_ids)

    def _add_or_modify_new_jobs(self, task, force=False):
        """
        add new jobs or modify existed jobs
        :return:
        """
        if not task.modified and not force:
            return

        task_job_ids = []
        clients = list(clients_of_task(task))
        # update for every client
        for client in clients:
            # get job id
            job_id = get_job_id(client, task)
            # add job_id to array
            task_job_ids.append(job_id)
            configuration = json.loads(task.configuration)
            trigger = task.trigger
            configuration = {arg: configuration.get(arg) for arg in args_map.get(trigger) if
                             configuration.get(arg)}
            logger.debug('adding or modifying job %s, trigger %s, configuration %s', job_id, trigger,
                         configuration)
            # if job doesn't exist, add it. otherwise replace it
            self.scheduler.add_job(execute, task.trigger, args=[client, task.project, task.spider], id=job_id,
                                   replace_existing=True, **configuration)

    def run(self):
        """
        heart beat detect
        :return:
        """
        self.sync_jobs(force=True)
        while True:
            self.sync_jobs()
            time.sleep(SCHEDULER_HEARTBEAT)


# init scheduler manager
sm = SchedulerManager(scheduler)

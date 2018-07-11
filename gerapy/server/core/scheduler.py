print("Scheduler？？？？？")
import json
from django_apscheduler.models import DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from gerapy.server.core.models import Client, Project, Task
print("Scheduler")

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

args_map = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date', 'timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}

def execute(client, project_name, spider_name):
    print('Execute', 'Client', client.name, 'Project Name',
          project_name, 'Spider Name', spider_name)


class SchedulerManager():
    def __init__(self, scheduler):
        self.scheduler = scheduler
        print('Events Registering')
        register_events(self.scheduler)
        print('Events Registered')

    def get_jobs(self):
        jobs = DjangoJob.objects.all()
        print('jobs', jobs)
        return jobs

    def get_tasks(self):
        tasks = Task.objects.all()
        print('Tasks')
        print(tasks)
        return tasks

    def get_clients(self, task):
        client_ids = json.loads(task.clients)
        print('Client ids', client_ids)
        for client_id in client_ids:
            client = Client.objects.get(id=client_id)
            if client:
                yield client

    def get_job_id(self, client_id, project_name, spider_name):
        return '%s-%s-%s' % (client_id, project_name, spider_name)

    def sync_jobs(self, tasks, jobs):
        for task in tasks:
            clients = list(self.get_clients(task))
            for client in clients:

                job_id = self.get_job_id(client.id, task.project, task.spider)
                print(job_id)
                configuration = json.loads(task.configuration)
                trigger = task.trigger
                print('trigger', trigger)
                configuration = {arg: configuration.get(arg) for arg in args_map.get(trigger)}
                print('configuration', configuration)
                
                self.scheduler.add_job(execute, task.trigger, args=[client, task.project, task.spider], id=job_id, **configuration)


    def run(self):
        print('Starting Scheduler')

        print('Started Scheduler')

        print('??????????')
        jobs = self.get_jobs()
        print(jobs)
        print('Getting tasks')
        tasks = self.get_tasks()
        print(tasks)
        self.sync_jobs(tasks, jobs)

        self.scheduler.start()


print('init job manager')
sm = SchedulerManager(scheduler)
print('inited')
sm.run()

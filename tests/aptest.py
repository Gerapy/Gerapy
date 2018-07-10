from apscheduler.schedulers.blocking import BlockingScheduler


def job_function():
    print("Hello World")


sched = BlockingScheduler()

# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
job = sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
print(job)

sched.start()

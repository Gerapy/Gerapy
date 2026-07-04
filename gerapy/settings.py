from os import getenv, getcwd
from os.path import join
import time

APP_DEBUG = getenv('APP_DEBUG', False)

# logs
LOG_ENABLED = getenv('LOG_ENABLED', True)
LOG_TO_CONSOLE = getenv('LOG_TO_CONSOLE', True)
LOG_TO_FILE = getenv('LOG_TO_FILE', True)
LOG_LEVEL = getenv('LOG_LEVEL', 'DEBUG' if APP_DEBUG else 'INFO')
LOG_DIR = getenv('LOG_DIR', 'logs')
LOG_FORMAT = getenv('LOG_FORMAT',
                    '%(levelname)s - %(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s')
LOG_PATH = join(getcwd(), LOG_DIR, time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.log')

# projects
PROJECTS_FOLDER = getenv('PROJECTS_FOLDER', 'projects')
LOGS_FOLDER = LOG_DIR
# scheduler
SCHEDULER_HEARTBEAT = 3
# apscheduler job defaults. The library defaults (misfire_grace_time=1s,
# max_instances=1) cause "Run time of job ... was missed!" warnings and skipped
# runs whenever the scheduler thread is briefly busy or a scrapyd request is
# slow. coalesce=True collapses several missed runs into a single one.
SCHEDULER_COALESCE = getenv('SCHEDULER_COALESCE', True)
SCHEDULER_MAX_INSTANCES = int(getenv('SCHEDULER_MAX_INSTANCES', 10))
SCHEDULER_MISFIRE_GRACE_TIME = int(getenv('SCHEDULER_MISFIRE_GRACE_TIME', 3600))

ADMINS = [
    'admin'
]

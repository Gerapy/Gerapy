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

ADMINS = [
    'admin'
]

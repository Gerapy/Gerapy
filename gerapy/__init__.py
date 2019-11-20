from os.path import abspath, dirname, exists, join
from os import makedirs
import logging
from gerapy import settings
import sys

version_file = dirname(abspath(__file__)) + '/VERSION'


def version():
    """
    get version from version file
    :return:
    """
    return open(version_file).read().strip()


loggers = {}


def get_logger(name=None, log_path=settings.LOG_PATH):
    """
    get logger by name and store it
    :param name:
    :return:
    """
    global loggers
    
    if not name:
        name = __name__
    
    if loggers.get(name):
        return loggers.get(name)
    
    # make log dir
    log_dir = dirname(log_path)
    if not exists(log_dir):
        makedirs(log_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # if log to console
    if settings.LOG_ENABLED and settings.LOG_TO_CONSOLE:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level=settings.LOG_LEVEL)
        formatter = logging.Formatter(settings.LOG_FORMAT)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    
    # if log to file
    if settings.LOG_ENABLED and settings.LOG_TO_FILE:
        # add file handler
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(level=settings.LOG_LEVEL)
        formatter = logging.Formatter(settings.LOG_FORMAT)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # add to loggers
    loggers[name] = logger
    
    return logger

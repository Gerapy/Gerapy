import configparser
from os.path import *

from gerapy.server.core.utils import merge


def config(path, section, option, name='scrapy.cfg', default=None):
    try:
        cf = configparser.ConfigParser()
        cfg_path = merge(path, name)
        cf.read(cfg_path)
        return cf.get(section, option)
    except configparser.NoOptionError:
        return default

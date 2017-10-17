import configparser
from os.path import join

def config(path, section, option, name='scrapy.cfg', default=None):
    try:
        cf = configparser.ConfigParser()
        cfg_path = join(path, name)
        cf.read(cfg_path)
        return cf.get(section, option)
    except configparser.NoOptionError:
        return default

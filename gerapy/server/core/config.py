import configparser
from os.path import join

def config(path, section, option, name='scrapy.cfg', default=None):
    """
    parse scrapy config
    :param path: config path
    :param section: config section
    :param option: other params
    :param name: file name
    :param default:
    :return:
    """
    try:
        cf = configparser.ConfigParser()
        cfg_path = join(path, name)
        cf.read(cfg_path)
        return cf.get(section, option)
    except configparser.NoOptionError:
        return default

from os.path import abspath, dirname

version_file = dirname(dirname(abspath(__file__))) + '/VERSION'

__version__ = open(version_file).read().strip()


def version():
    return __version__
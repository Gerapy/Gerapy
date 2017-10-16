from os.path import abspath, dirname

version_file = dirname(abspath(__file__)) + '/VERSION'

def version():
    return open(version_file).read().strip()

from setuptools import setup, find_packages
from os.path import join, isfile
from os import walk
import gerapy


def read_file(filename):
    """
    return file content
    :param filename:
    :return:
    """
    with open(filename) as fp:
        return fp.read().strip()

def read_requirements(filename):
    """
    get requirements for gerapy
    :param filename:
    :return:
    """
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


def package_files(directories):
    """
    get relative path of files in directories
    :param directories:
    :return:
    """
    paths = []
    for item in directories:
        if isfile(item):
            paths.append(join('..', item))
            continue
        for (path, directories, filenames) in walk(item):
            for filename in filenames:
                paths.append(join('..', path, filename))
    return paths


setup(
    name='gerapy',
    version=gerapy.version(),
    description='distributed crawler',
    keywords=['gerapy', 'scrapy', 'distributed'],
    author='germey',
    author_email='cqc@cuiqingcai.com',
    url='http://pypi.python.org/pypi/gerapy/',
    license='MIT',
    install_requires=read_requirements('requirements.txt'),
    packages=find_packages(),
    entry_points={
        'console_scripts': ['gerapy = gerapy.cmd:cmd']
    },
    package_data={
        '': package_files([
            'gerapy/server/static',
            'gerapy/server/core/templates',
            'gerapy/templates',
            'gerapy/VERSION'
        ])
    },
    publish=[
        'sudo python3 setup.py bdist_egg',
        'sudo python3 setup.py sdist',
        'sudo python3 setup.py bdist_egg upload'
        'sudo python3 setup.py sdist upload'
    ]
)

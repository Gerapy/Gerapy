import io
from setuptools import setup, find_packages
import gerapy


def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='gerapy',
    version=gerapy.__version__,
    description='distributed crawler',
    keywords='gerapy',
    author='germey',
    url='gerapy.com',
    license='MIT',
    install_requires=read_requirements('requirements.txt'),
    packages=find_packages(),
    entry_points={
        'console_scripts': ['gerapy = gerapy.cmd:cmd']
    },
    package_data={
        'gerapy': [
            'server/static/**/*.*',
            'server/core/templates/*.*',
            'server/core/templates/**/*.*'
        ],
    },
)

import io
from setuptools import setup, find_packages

def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='gerapy',
    version=read_file('VERSION'),
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
        'gerapy': [
            'server/static/**/*.*',
            'server/core/templates/*.*',
            'server/core/templates/**/*.*',
            'server/core/templates/static/css/*.*',
            'server/core/templates/static/fonts/*.*',
            'server/core/templates/static/images/*.*',
            'server/core/templates/static/js/*.*'
        ],
    },
    publish=[
        'python setup.py bdist_egg',
        'python setup.py sdist',
        'python setup.py bdist_egg upload'
        'python setup.py sdist upload'
    ]
)

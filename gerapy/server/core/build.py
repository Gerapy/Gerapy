import sys
import os
import glob
import tempfile
import shutil

from gerapy import get_logger
from gerapy.cmd.init import PROJECTS_FOLDER
from gerapy.server.core.config import config
from os.path import join
from subprocess import check_call
from scrapy.utils.python import retry_on_eintr

logger = get_logger(__name__)


def build_project(project):
    """
    build project
    :param project:
    :return:
    """
    egg = build_egg(project)
    logger.info('successfully build project %s to egg file %s', project, egg)
    return egg


_SETUP_PY_TEMPLATE = \
    '''# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='%(project)s',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy':['settings=%(settings)s']},
)'''


# build Egg
def build_egg(project):
    '''
    build project to egg file
    :param project: 
    :return: 
    '''
    work_path = os.getcwd()
    try:
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        project_path = join(path, project)
        os.chdir(project_path)
        settings = config(project_path, 'settings', 'default')
        create_default_setup_py(project_path, settings=settings, project=project)
        d = tempfile.mkdtemp(prefix='gerapy-')
        o = open(os.path.join(d, 'stdout'), 'wb')
        e = open(os.path.join(d, 'stderr'), 'wb')
        retry_on_eintr(check_call, [sys.executable, 'setup.py', 'clean', '-a', 'bdist_egg', '-d', d],
                       stdout=o, stderr=e)
        o.close()
        e.close()
        egg = glob.glob(os.path.join(d, '*.egg'))[0]
        # Delete Origin file
        if find_egg(project_path):
            os.remove(join(project_path, find_egg(project_path)))
        shutil.move(egg, project_path)
        return join(project_path, find_egg(project_path))
    except Exception as e:
        logger.error('error occurred %s', e.args)
    finally:
        os.chdir(work_path)


def find_egg(path):
    """
    find egg from path
    :param path:
    :return:
    """
    items = os.listdir(path)
    for name in items:
        if name.endswith('.egg'):
            return name


def create_default_setup_py(path, **kwargs):
    """
    create setup.py file to path
    :param path:
    :param kwargs:
    :return:
    """
    with open(join(path, 'setup.py'), 'w', encoding='utf-8') as f:
        file = _SETUP_PY_TEMPLATE % kwargs
        f.write(file)
        f.close()
        logger.debug('successfully created setup.py file at %s', path)

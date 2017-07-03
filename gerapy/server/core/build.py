import sys
import os
import glob
import tempfile
import shutil
from gerapy.cmd.init import PROJECTS_FOLDER
from gerapy.server.core.config import config
from gerapy.server.core.utils import merge
from subprocess import check_call
from scrapy.utils.python import retry_on_eintr


# 构建项目
def build_project(project):
    egg = build_egg(project)
    print('Built %(project)s into %(egg)s' % {'egg': egg, 'project': project})
    return egg


_SETUP_PY_TEMPLATE = \
    """# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='%(project)s',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy':['settings=%(settings)s']},
)"""


# 构建Egg
def build_egg(project):
    work_path = os.getcwd()
    try:
        path = os.path.abspath(merge(os.getcwd(), PROJECTS_FOLDER))
        print('Path', path)
        project_path = merge(path, project)
        os.chdir(project_path)
        settings = config(project_path, 'settings', 'default')
        print('Settings', settings)
        create_default_setup_py(project_path, settings=settings, project=project)
        d = tempfile.mkdtemp(prefix="gerapy-")
        o = open(os.path.join(d, "stdout"), "wb")
        e = open(os.path.join(d, "stderr"), "wb")
        retry_on_eintr(check_call, [sys.executable, 'setup.py', 'clean', '-a', 'bdist_egg', '-d', d],
                       stdout=o, stderr=e)
        o.close()
        e.close()
        egg = glob.glob(os.path.join(d, '*.egg'))[0]
        # 删除原文件
        if find_egg(project_path):
            os.remove(merge(project_path, find_egg(project_path)))
        shutil.move(egg, project_path)
        return merge(project_path, find_egg(project_path))
    except Exception as e:
        print(e.args)
    finally:
        os.chdir(work_path)


# 查找某路径下的Egg文件
def find_egg(path):
    items = os.listdir(path)
    for name in items:
        if name.endswith(".egg"):
            return name
    return None


# 创建setup.py
def create_default_setup_py(path, **kwargs):
    with open(merge(path, 'setup.py'), 'w') as f:
        print(kwargs)
        file = _SETUP_PY_TEMPLATE % kwargs
        print(file)
        f.write(file)
        f.close()

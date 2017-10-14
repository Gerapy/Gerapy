from __future__ import print_function
import re
import os
import string
from importlib import import_module
from os.path import join, exists, abspath
from shutil import ignore_patterns, move, copy2, copystat

import scrapy
from scrapy.commands import ScrapyCommand
from scrapy.utils.template import render_templatefile, string_camelcase
from scrapy.exceptions import UsageError

TEMPLATES_DIR = './templates/project'

TEMPLATES_TO_RENDER = (
    ('scrapy.cfg',),
    ('${project_name}', 'settings.py.tmpl'),
    ('${project_name}', 'items.py.tmpl'),
    ('${project_name}', 'pipelines.py.tmpl'),
    ('${project_name}', 'middlewares.py.tmpl'),
)

IGNORE = ignore_patterns('*.pyc', '.svn', '.git')


def is_valid_name(project_name):
    if not re.search(r'^[_a-zA-Z]\w*$', project_name):
        print('Error: Project Name must begin with a letter and contain only letters, numbers and underscores')
        return False
    return True


def copytree(src, dst):
    ignore = IGNORE
    names = os.listdir(src)
    ignored_names = ignore(src, names)
    
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for name in names:
        if name in ignored_names:
            continue
        
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        if os.path.isdir(srcname):
            copytree(srcname, dstname)
        else:
            copy2(srcname, dstname)
    copystat(src, dst)


def run(project_name, project_dir):
    if not is_valid_name(project_name):
        return
    print(abspath(TEMPLATES_DIR), abspath(project_dir))
    copytree(abspath(TEMPLATES_DIR), abspath(project_dir))
    move(join(project_dir, 'module'), join(project_dir, project_name))
    for paths in TEMPLATES_TO_RENDER:
        path = join(*paths)
        tplfile = join(project_dir,
                       string.Template(path).substitute(project_name=project_name))
        render_templatefile(tplfile, project_name=project_name,
                            ProjectName=string_camelcase(project_name))
    print("New Scrapy project %r, using template directory:" % \
          (project_name))
    print("    %s\n" % abspath(project_dir))
    print("You can start your first spider with:")
    print("    cd %s" % project_dir)
    print("    scrapy genspider example example.com")


if __name__ == '__main__':
    run('news', '.')

import fnmatch
import re
import os
from os.path import join, abspath, dirname
from shutil import ignore_patterns, copy2, copystat
from jinja2 import Template

IGNORES = ['.git/', '*.pyc', '.DS_Store', '.idea/']


def scrapyd_url(ip, port):
    url = 'http://{ip}:{port}'.format(ip=ip, port=port)
    return url


def log_url(ip, port, project, spider, job):
    url = 'http://{ip}:{port}/logs/{project}/{spider}/{job}.log'.format(ip=ip, port=port, project=project,
                                                                        spider=spider, job=job)
    return url


def merge(path, file):
    return '{0}/{1}'.format(path, file)


def ignored(ignores, path, file):
    file_name = join(path, file)
    for ignore in ignores:
        if '/' in ignore and ignore.rstrip('/') in file_name:
            return True
        if fnmatch.fnmatch(file_name, ignore):
            return True
        if file == ignore:
            return True
    return False


def get_tree(path, ignores=IGNORES):
    result = []
    for file in os.listdir(path):
        if os.path.isdir(join(path, file)):
            if not ignored(ignores, path, file):
                children = get_tree(join(path, file), ignores)
                if children:
                    result.append({
                        'label': file,
                        'children': children,
                        'path': path
                    })
        else:
            if not ignored(ignores, path, file):
                result.append({'label': file, 'path': path})
    return result


TEMPLATES_DIR = join(dirname(dirname(dirname(abspath(__file__)))), 'templates')

TEMPLATES_TO_RENDER = (
    ('scrapy.cfg',),
    ('${project_name}', 'settings.py.tmpl'),
    ('${project_name}', 'items.py.tmpl'),
    ('${project_name}', 'pipelines.py.tmpl'),
    ('${project_name}', 'middlewares.py.tmpl'),
)


def is_valid_name(project_name):
    if not re.search(r'^[_a-zA-Z]\w*$', project_name):
        print('Error: Project Name must begin with a letter and contain only letters, numbers and underscores')
        return False
    return True


def copytree(src, dst):
    ignore = ignore_patterns(*IGNORES)
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


def render_templatefile(tpl_file, dst_file, *args, **kwargs):
    vars = dict(*args, **kwargs)
    template = Template(open(tpl_file).read())
    os.remove(tpl_file)
    result = template.render(vars)
    print('Render Result', result)
    open(dst_file, 'w').write(result)

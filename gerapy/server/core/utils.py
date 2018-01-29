import fnmatch
import re
import os
import traceback
from os.path import join, abspath, dirname
from shutil import ignore_patterns, copy2, copystat
from jinja2 import Template
from scrapyd_api import ScrapydAPI

IGNORES = ['.git/', '*.pyc', '.DS_Store', '.idea/', '*.egg', '*.egg-info/', '*.egg-info', 'build/']

TEMPLATES_DIR = join(dirname(dirname(dirname(abspath(__file__)))), 'templates')

TEMPLATES_TO_RENDER = (
    ('scrapy.cfg',),
    ('${project_name}', 'settings.py.tmpl'),
    ('${project_name}', 'items.py.tmpl'),
    ('${project_name}', 'pipelines.py.tmpl'),
    ('${project_name}', 'middlewares.py.tmpl'),
)


def get_scrapyd(client):
    if not client.auth:
        return ScrapydAPI(scrapyd_url(client.ip, client.port))
    return ScrapydAPI(scrapyd_url(client.ip, client.port), auth=(client.username, client.password))


def scrapyd_url(ip, port):
    """
    get scrapyd url
    :param ip: host
    :param port: port
    :return: string
    """
    url = 'http://{ip}:{port}'.format(ip=ip, port=port)
    return url


def log_url(ip, port, project, spider, job):
    """
    get log url
    :param ip: host
    :param port: port
    :param project: project
    :param spider: spider
    :param job: job
    :return: string
    """
    url = 'http://{ip}:{port}/logs/{project}/{spider}/{job}.log'.format(ip=ip, port=port, project=project,
                                                                        spider=spider, job=job)
    return url


def ignored(ignores, path, file):
    """
    judge if the file is ignored
    :param ignores: ignored list
    :param path: file path
    :param file: file name
    :return: bool
    """
    file_name = join(path, file)
    for ignore in ignores:
        if '/' in ignore and ignore.rstrip('/') in file_name:
            return True
        if fnmatch.fnmatch(file_name, ignore):
            return True
        if file == ignore:
            return True
    return False


def is_valid_name(project_name):
    """
    judge name is valid
    :param project_name:
    :return:
    """
    if not re.search(r'^[_a-zA-Z]\w*$', project_name):
        print('Error: Project Name must begin with a letter and contain only letters, numbers and underscores')
        return False
    return True


def copy_tree(src, dst):
    """
    copy tree
    :param src:
    :param dst:
    :return:
    """
    ignore = ignore_patterns(*IGNORES)
    names = os.listdir(src)
    ignored_names = ignore(src, names)
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for name in names:
        if name in ignored_names:
            continue
        
        src_name = os.path.join(src, name)
        dst_name = os.path.join(dst, name)
        if os.path.isdir(src_name):
            copy_tree(src_name, dst_name)
        else:
            copy2(src_name, dst_name)
    copystat(src, dst)


def get_tree(path, ignores=IGNORES):
    """
    get tree structure
    :param path: Folder path
    :param ignores: Ignore files
    :return: Json
    """
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


def render_template(tpl_file, dst_file, *args, **kwargs):
    """
    render template
    :param tpl_file: Template file name
    :param dst_file: Destination file name
    :param args: args
    :param kwargs: kwargs
    :return: None
    """
    vars = dict(*args, **kwargs)
    template = Template(open(tpl_file).read())
    os.remove(tpl_file)
    result = template.render(vars)
    print(result)
    
    open(dst_file, 'w').write(result)


def get_traceback():
    """
    get last line of error
    :return: String
    """
    info = traceback.format_exc(limit=1)
    if info:
        info = info.splitlines()
        info = list(filter(lambda x: x, info))
        if len(info):
            return info[-1]
        return None
    return info

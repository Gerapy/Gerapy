import fnmatch
import multiprocessing
import re
from copy import deepcopy
import subprocess
from subprocess import Popen, PIPE, STDOUT
from os.path import abspath
from shutil import ignore_patterns, copy2, copystat
from jinja2 import Template
from scrapyd_api import ScrapydAPI
from bs4 import BeautifulSoup
import traceback
import json, os, string
from shutil import move, copy, rmtree
from os.path import join, exists, dirname
from django.forms.models import model_to_dict
from django.utils import timezone
from gerapy.cmd.init import PROJECTS_FOLDER
from gerapy.server.core.models import Project

IGNORES = ['.git/', '*.pyc', '.DS_Store', '.idea/', '*.egg', '*.egg-info/', '*.egg-info', 'build/']

TEMPLATES_DIR = join(dirname(dirname(dirname(abspath(__file__)))), 'templates')

TEMPLATES_TO_RENDER = (
    ('scrapy.cfg',),
    ('${project_name}', 'settings.py.tmpl'),
    ('${project_name}', 'items.py.tmpl'),
    ('${project_name}', 'pipelines.py.tmpl'),
    ('${project_name}', 'middlewares.py.tmpl'),
)

NO_REFERRER = '<meta name="referrer" content="never">'
BASE = '<base href="{href}">'


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


def process_request(request):
    """
    process request
    :param request:
    :return:
    """
    return {
        'url': request.url,
        'method': request.method,
        'meta': request.meta,
        'headers': request.headers,
        'callback': request.callback
    }


def process_response(response):
    """
    process response to dict
    :param response:
    :return:
    """
    return {
        'html': response.text,
        'url': response.url,
        'status': response.status
    }


def process_item(item):
    return dict(item)


def process_html(html, base_url):
    """
    process html, add some tricks such as no referrer
    :param html: source html
    :return: processed html
    """
    dom = BeautifulSoup(html, 'lxml')
    dom.find('head').insert(0, BeautifulSoup(NO_REFERRER, 'lxml'))
    dom.find('head').insert(0, BeautifulSoup(BASE.format(href=base_url), 'lxml'))
    html = str(dom)
    # html = unescape(html)
    return html


def get_output_error(project_name, spider_name):
    """
    get scrapy runtime error
    :param project_name: project name
    :param spider_name: spider name
    :return: output, error
    """
    work_cwd = os.getcwd()
    project_path = join(PROJECTS_FOLDER, project_name)
    try:
        os.chdir(project_path)
        cmd = ' '.join(['scrapy', 'crawl', spider_name])
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read()
        if isinstance(output, bytes):
            output = output.decode('utf-8')
        return output
    finally:
        os.chdir(work_cwd)


def get_items_configuration(configuration):
    """
    get items configuration including allowed_spiders and tables or collections
    :param configuration: configuration data
    :return: items
    """
    configuration = deepcopy(configuration)
    items = configuration.get('items')
    spiders = configuration.get('spiders')
    for spider in spiders:
        # MongoDB
        mongodb_collection_map = spider.get('storage').get('mongodb').get('collections')
        for mongodb_collection_map_item in mongodb_collection_map:
            collection = mongodb_collection_map_item.get('collection')
            item_name = mongodb_collection_map_item.get('item')
            for item in items:
                if item.get('name') == item_name:
                    allowed_spiders = item.get('mongodb_spiders', set())
                    allowed_spiders.add(spider.get('name'))
                    mongodb_collections = item.get('mongodb_collections', set())
                    mongodb_collections.add(collection)
                    item['mongodb_spiders'], item['mongodb_collections'] = allowed_spiders, mongodb_collections
        
        # MySQL
        mysql_table_map = spider.get('storage').get('mysql').get('tables')
        for mysql_table_map_item in mysql_table_map:
            collection = mysql_table_map_item.get('table')
            item_name = mysql_table_map_item.get('item')
            for item in items:
                if item.get('name') == item_name:
                    allowed_spiders = item.get('mysql_spiders', set())
                    allowed_spiders.add(spider.get('name'))
                    mysql_tables = item.get('mysql_tables', set())
                    mysql_tables.add(collection)
                    item['mysql_spiders'], item['mysql_tables'] = allowed_spiders, mysql_tables
    # transfer attr
    attrs = ['mongodb_spiders', 'mongodb_collections', 'mysql_spiders', 'mysql_tables']
    for item in items:
        for attr in attrs:
            item[attr] = list(item[attr])
    return items


def generate_project(project_name):
    """
    generate project code
    :param project_name: project name
    :return: project data
    """
    
    def generate(project_name, result):
        # get configuration
        configuration = Project.objects.get(name=project_name).configuration
        configuration = json.loads(configuration)
        # remove original project dir
        project_dir = join(PROJECTS_FOLDER, project_name)
        if exists(project_dir):
            rmtree(project_dir)
        # generate project
        copy_tree(join(TEMPLATES_DIR, 'project'), project_dir)
        move(join(PROJECTS_FOLDER, project_name, 'module'), join(project_dir, project_name))
        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tplfile = join(project_dir,
                           string.Template(path).substitute(project_name=project_name))
            items = get_items_configuration(configuration)
            print('Items', items)
            vars = {
                'project_name': project_name,
                'items': items,
            }
            render_template(tplfile, tplfile.rstrip('.tmpl'), **vars)
        # generate spider
        spiders = configuration.get('spiders')
        for spider in spiders:
            source_tpl_file = join(TEMPLATES_DIR, 'spiders', 'crawl.tmpl')
            new_tpl_file = join(PROJECTS_FOLDER, project_name, project_name, 'spiders', 'crawl.tmpl')
            spider_file = "%s.py" % join(PROJECTS_FOLDER, project_name, project_name, 'spiders', spider.get('name'))
            copy(source_tpl_file, new_tpl_file)
            render_template(new_tpl_file, spider_file, spider=spider, project_name=project_name)
        # save generated_at attr
        model = Project.objects.get(name=project_name)
        model.generated_at = timezone.now()
        # clear built_at attr
        model.built_at = None
        model.save()
        # return model
        result['data'] = model_to_dict(model)
    
    try:
        # new manager
        manager = multiprocessing.Manager()
        result = manager.dict()
        jobs = []
        # use Process in case of reactor stop exception
        p = multiprocessing.Process(target=generate, args=(project_name, result))
        jobs.append(p)
        p.start()
        # processes
        for proc in jobs:
            proc.join()
        print('Data', result['data'])
        return result['data']
    except FileNotFoundError as e:
        print('Processing', e.args)
        return None

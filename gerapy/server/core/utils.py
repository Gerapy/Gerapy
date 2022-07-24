import fnmatch
import re
from copy import deepcopy
from furl import furl
from subprocess import Popen, PIPE, STDOUT
from os.path import abspath
from shutil import ignore_patterns, copy2, copystat
from jinja2 import Template
from scrapyd_api import ScrapydAPI
from bs4 import BeautifulSoup
import traceback
import json
import os
import string
from shutil import move, copy, rmtree
from os.path import join, exists, dirname
from django.utils import timezone
from gerapy import get_logger
from gerapy.settings import PROJECTS_FOLDER


IGNORES = ['.git/', '*.pyc', '.DS_Store', '.idea/',
           '*.egg', '*.egg-info/', '*.egg-info', 'build/']

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
    logger = get_logger(__name__)
    if not re.search(r'^[_a-zA-Z]\w*$', project_name):
        logger.error('project name %s must begin with a letter and contain only letters, numbers and underscores',
                     project_name)
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
    template = Template(open(tpl_file, encoding='utf-8').read())
    os.remove(tpl_file)
    result = template.render(vars)
    open(dst_file, 'w', encoding='utf-8').write(result)


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
    result = {
        'url': request.url,
        'method': request.method,
        'meta': request.meta,
        'callback': request.callback,
        'cookies': request.cookies,
        'headers': request.headers,
        'priority': request.priority,
        'dont_filter': request.dont_filter,
    }
    # set body
    if request.method.lower() != 'get':
        result['body'] = request.body
        if isinstance(result['body'], bytes):
            result['body'] = result['body'].decode('utf-8')
        result['body'] = str2body(result['body'])
    return result


def process_response(response):
    """
    process response to dict
    :param response:
    :return:
    """
    return {
        'html': process_html(response.text, furl(response.url).origin),
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
    dom.find('head').insert(0, BeautifulSoup(
        BASE.format(href=base_url), 'lxml'))
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
        p = Popen(cmd, shell=False, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT, close_fds=True)
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
        mongodb_collection_map = spider.get(
            'storage').get('mongodb').get('collections')
        for mongodb_collection_map_item in mongodb_collection_map:
            collection = mongodb_collection_map_item.get('collection')
            item_name = mongodb_collection_map_item.get('item')
            for item in items:
                if item.get('name') == item_name:
                    allowed_spiders = item.get('mongodb_spiders', set())
                    allowed_spiders.add(spider.get('name'))
                    mongodb_collections = item.get(
                        'mongodb_collections', set())
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
    attrs = ['mongodb_spiders', 'mongodb_collections',
             'mysql_spiders', 'mysql_tables']
    for item in items:
        for attr in attrs:
            if item.get(attr):
                item[attr] = list(item[attr])
    return items


def process_custom_settings(spider):
    """
    process custom settings of some config items
    :param spider:
    :return:
    """
    custom_settings = spider.get('custom_settings')

    def add_dict_to_custom_settings(custom_settings, keys):
        """
        if config doesn't exist, add default value
        :param custom_settings:
        :param keys:
        :return:
        """
        for key in keys:
            for item in custom_settings:
                if item['key'] == key:
                    break
            else:
                custom_settings.append({
                    'key': key,
                    'value': '{}'
                })
        return custom_settings

    keys = ['DOWNLOADER_MIDDLEWARES', 'SPIDER_MIDDLEWARES', 'ITEM_PIPELINES']
    custom_settings = add_dict_to_custom_settings(custom_settings, keys)
    for item in custom_settings:

        if item['key'] == 'DOWNLOADER_MIDDLEWARES':
            item_data = json.loads(item['value'])
            if spider.get('cookies', {}).get('enable', {}):
                item_data[
                    'gerapy.downloadermiddlewares.cookies.CookiesMiddleware'] = 554
            if spider.get('proxy', {}).get('enable', {}):
                item_data[
                    'gerapy.downloadermiddlewares.proxy.ProxyMiddleware'] = 555
            item_data['gerapy.downloadermiddlewares.pyppeteer.PyppeteerMiddleware'] = 601
            item_data['scrapy_splash.SplashCookiesMiddleware'] = 723
            item_data['scrapy_splash.SplashMiddleware'] = 725
            item_data['scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware'] = 810
            item['value'] = json.dumps(item_data)
        if item['key'] == 'SPIDER_MIDDLEWARES':
            item_data = json.loads(item['value'])
            item_data['scrapy_splash.SplashDeduplicateArgsMiddleware'] = 100
            item['value'] = json.dumps(item_data)
        if item['key'] == 'ITEM_PIPELINES':
            item_data = json.loads(item['value'])
            if spider.get('storage', {}).get('mysql', {}).get('enable', {}):
                item_data[
                    'gerapy.pipelines.MySQLPipeline'] = 300
            if spider.get('storage', {}).get('mongodb', {}).get('enable', {}):
                item_data[
                    'gerapy.pipelines.MongoDBPipeline'] = 301
            item['value'] = json.dumps(item_data)
    return spider


def generate_project(project_name):
    """
    generate project code
    :param project_name: project name
    :return: project data
    """
    # get configuration
    from gerapy.server.core.models import Project
    configuration = Project.objects.get(name=project_name).configuration
    configuration = json.loads(configuration)
    # remove original project dir
    project_dir = join(PROJECTS_FOLDER, project_name)
    if exists(project_dir):
        rmtree(project_dir)
    # generate project
    copy_tree(join(TEMPLATES_DIR, 'project'), project_dir)
    move(join(PROJECTS_FOLDER, project_name, 'module'),
         join(project_dir, project_name))
    for paths in TEMPLATES_TO_RENDER:
        path = join(*paths)
        tplfile = join(project_dir,
                       string.Template(path).substitute(project_name=project_name))
        items = get_items_configuration(configuration)
        vars = {
            'project_name': project_name,
            'items': items,
        }
        render_template(tplfile, tplfile.rstrip('.tmpl'), **vars)
    # generate spider
    spiders = configuration.get('spiders')
    for spider in spiders:
        spider = process_custom_settings(spider)
        source_tpl_file = join(TEMPLATES_DIR, 'spiders', 'crawl.tmpl')
        new_tpl_file = join(PROJECTS_FOLDER, project_name,
                            project_name, 'spiders', 'crawl.tmpl')
        spider_file = "%s.py" % join(
            PROJECTS_FOLDER, project_name, project_name, 'spiders', spider.get('name'))
        copy(source_tpl_file, new_tpl_file)
        render_template(new_tpl_file, spider_file,
                        spider=spider, project_name=project_name)
    # save generated_at attr
    model = Project.objects.get(name=project_name)
    model.generated_at = timezone.now()
    # clear built_at attr
    model.built_at = None
    model.save()


def bytes2str(data):
    """
    bytes2str
    :param data: origin data
    :return: str
    """
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    data = data.strip()
    return data


def clients_of_task(task):
    """
    get valid clients of task
    :param task: task object
    :return:
    """
    from gerapy.server.core.models import Client
    client_ids = json.loads(task.clients)
    for client_id in client_ids:
        client = Client.objects.get(id=client_id)
        if client:
            yield client


def get_job_id(client, task):
    """
    construct job id
    :param client: client object
    :param task: task object
    :return: job id
    """
    return '%s-%s-%s' % (client.name, task.project, task.spider)


def load_dict(x, transformer=None):
    """
    convert to  dict
    :param x:
    :return:
    """
    if x is None or isinstance(x, dict):
        return x
    try:
        data = json.loads(x)
        if not transformer:
            def transformer(x): return x
        data = {k: transformer(v) for k, v in data.items()}
        return data
    except:
        return {}


def str2list(x, transformer=None):
    """
    convert to list
    :param x:
    :return:
    """
    if x is None or isinstance(x, list):
        return x
    try:
        data = json.loads(x)
        if not transformer:
            def transformer(x): return x
        data = list(map(lambda x: transformer(x), data))
        return data
    except:
        return []


def str2bool(v):
    """
    convert string to bool
    :param v:
    :return:
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    return True


def str2json(v):
    """
    convert str to json data
    :param v:
    :return:
    """
    try:
        return json.loads(v)
    except:
        return None


def str2dict(v):
    """
    convert str to dict data
    :param v:
    :return:
    """
    try:
        return json.loads(v)
    except:
        return {}


def str2body(v):
    """
    convert str to json data or keep original string
    :param v:
    :return:
    """
    try:
        return json.loads(v)
    except:
        return v


def str2str(v):
    """
    convert str to str, process for 'None', 'null', '',
    :param v:
    :return:
    """
    if v.lower() in ('none', 'null', 'undefined', 'nil', 'false'):
        return None
    return str(v)


def log_exception(exception=Exception, logger=None):
    """
    used for log exceptions
    """
    if not logger:
        logger = get_logger(__name__)

    def deco(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except exception as err:
                logger.exception(err, exc_info=True)
            else:
                return result
        return wrapper
    return deco


def is_in_curdir(filepath):
    """
    return if a filepath in cur directory
    """
    execute_path = os.getcwd()
    print('ecec', execute_path, filepath)
    result = os.path.realpath(filepath).startswith(
        os.path.realpath(execute_path))
    print('result', result)
    return result

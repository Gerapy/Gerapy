import json
import os
import requests
import shutil
import sys
import time
import pytz
import pymongo
import string
import traceback
from django.shortcuts import render
from gerapy.server.core.build import build_project, find_egg
from gerapy.server.core.encoder import JSONEncoder
from gerapy.server.core.time import DATE_TIME_FORMAT
from gerapy.server.core.utils import IGNORES, is_valid_name, copytree, TEMPLATES_DIR, TEMPLATES_TO_RENDER, \
    render_templatefile, get_traceback
from gerapy.cmd.init import PROJECTS_FOLDER
from gerapy.server.core.utils import scrapyd_url, log_url, get_tree, merge
from gerapy.server.core.models import Client, Project, Deploy, Monitor
from django.core.serializers import serialize
from django.http import HttpResponse
from django.forms.models import model_to_dict
from scrapyd_api import ScrapydAPI
from requests.exceptions import ConnectionError
from os.path import join, abspath, exists
from shutil import move, copy
from gerapy.server.server.settings import TIME_ZONE
from datetime import datetime
from scrapy.utils.template import string_camelcase
from django.utils import timezone
from gerapy.server.core.response import JsonResponse


def index(request):
    return render(request, 'index.html')


def client_index(request):
    return HttpResponse(serialize('json', Client.objects.order_by('-id')))


def client_show(request, id):
    if request.method == 'GET':
        return HttpResponse(json.dumps(model_to_dict(Client.objects.get(id=id)), cls=JSONEncoder))


def client_status(request, id):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        try:
            requests.get(scrapyd_url(client.ip, client.port), timeout=3)
            return HttpResponse('1')
        except ConnectionError:
            return HttpResponse('0')


def client_update(request, id):
    if request.method == 'POST':
        client = Client.objects.filter(id=id)
        data = json.loads(request.body)
        client.update(**data)
        return HttpResponse(json.dumps(model_to_dict(Client.objects.get(id=id)), cls=JSONEncoder))


def index_status(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        data = {
            'success': 0,
            'error': 0,
            'project': 0,
        }
        for client in clients:
            try:
                requests.get(scrapyd_url(client.ip, client.port), timeout=1)
                data['success'] += 1
            except ConnectionError:
                data['error'] += 1
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        files = os.listdir(path)
        for file in files:
            if os.path.isdir(join(path, file)) and not file in IGNORES:
                data['project'] += 1
        return HttpResponse(json.dumps(data, cls=JSONEncoder))


def client_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client = Client.objects.create(**data)
        return HttpResponse(json.dumps(model_to_dict(client), cls=JSONEncoder))


def client_remove(request, id):
    if request.method == 'POST':
        Client.objects.filter(id=id).delete()
        return HttpResponse(json.dumps('1'))


def spider_list(request, id, project):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        spiders = scrapyd.list_spiders(project)
        spiders = [{'name': spider, 'id': index + 1} for index, spider in enumerate(spiders)]
        return HttpResponse(json.dumps(spiders))


def spider_start(request, id, project, spider):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.schedule(project, spider)
        return HttpResponse(json.dumps({'job': result}))


def project_list(request, id):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        projects = scrapyd.list_projects()
        return HttpResponse(json.dumps(projects))


def project_index(request):
    if request.method == 'GET':
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        files = os.listdir(path)
        project_list = []
        for file in files:
            if os.path.isdir(join(path, file)) and not file in IGNORES:
                project_list.append({'name': file})
        return HttpResponse(json.dumps(project_list))


def project_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data['configurable'] = 1
        Project.objects.update_or_create(**data)
        return HttpResponse(data.get('name'))


def project_configure(request, name):
    """
    get or update configuration
    :param request:
    :param name:
    :return:
    """
    if request.method == 'GET':
        project = Project.objects.get(name=name)
        project = model_to_dict(project)
        project['configuration'] = json.loads(project['configuration'])
        return HttpResponse(json.dumps(project, cls=JSONEncoder))
    elif request.method == 'POST':
        project = Project.objects.filter(name=name)
        data = json.loads(request.body)
        configuration = json.dumps(data.get('configuration'))
        project.update(**{'configuration': configuration})
        project = Project.objects.get(name=name)
        project = model_to_dict(project)
        return HttpResponse('1')


def project_tree(request, project_name):
    """
    get file tree of project
    :param request: Request object
    :param project_name: Project name
    :return: JsonResponse of tree
    """
    if request.method == 'GET':
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        # get tree data
        tree = get_tree(join(path, project_name))
        return JsonResponse(tree)


def project_remove(request, project_name):
    """
    remove project from disk and db
    :param request: Request object
    :param project_name: Project name
    :return:
    """
    if request.method == 'POST':
        path = join(os.path.abspath(os.getcwd()), PROJECTS_FOLDER)
        project_path = join(path, project_name)
        # delete project file tree
        shutil.rmtree(project_path)
        # delete project
        result = Project.objects.filter(name=project_name).delete()
        return JsonResponse({'result': result})


def project_version(request, client_id, project_name):
    """
    get project deploy version
    :param request: Request object
    :param client_id: Client id
    :param project_name: Project name
    :return:
    """
    if request.method == 'GET':
        # get client and project model
        client = Client.objects.get(id=client_id)
        project = Project.objects.get(name=project_name)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        # if deploy info exists in db, return it
        if Deploy.objects.filter(client=client, project=project):
            deploy = Deploy.objects.get(client=client, project=project)
        # if deploy info does not exists in db, create deploy info
        else:
            try:
                versions = scrapyd.list_versions(project_name)
            except requests.exceptions.ConnectionError:
                return JsonResponse({'message': 'Connect Error'}, status=500)
            if len(versions) > 0:
                version = versions[-1]
                deployed_at = timezone.datetime.fromtimestamp(int(version), tz=pytz.timezone(TIME_ZONE))
            else:
                deployed_at = None
            deploy, result = Deploy.objects.update_or_create(client=client, project=project, deployed_at=deployed_at)
        # return deploy json info
        return JsonResponse(model_to_dict(deploy))


def project_deploy(request, client_id, project_name):
    """
    deploy project operation
    :param request: Request object
    :param client_id: Client id
    :param project_name: Project name
    :return: JsonResponse
    """
    if request.method == 'POST':
        # get project folder
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        project_path = join(path, project_name)
        # find egg file
        egg = find_egg(project_path)
        egg_file = open(join(project_path, egg), 'rb')
        # get client and project model
        client = Client.objects.get(id=client_id)
        project = Project.objects.get(name=project_name)
        # execute deploy operation
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        try:
            scrapyd.add_version(project_name, int(time.time()), egg_file.read())
            # update deploy info
            deployed_at = timezone.now()
            Deploy.objects.filter(client=client, project=project).delete()
            deploy, result = Deploy.objects.update_or_create(client=client, project=project, deployed_at=deployed_at,
                                                             description=project.description)
            return JsonResponse(model_to_dict(deploy))
        except Exception:
            return JsonResponse({'message': get_traceback()}, status=500)


def project_build(request, project_name):
    """
    get build info or execute build operation
    :param request: Request object
    :param project_name: Project name
    :return: JsonResponse
    """
    # get project folder
    path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
    project_path = join(path, project_name)
    # get build version
    if request.method == 'GET':
        egg = find_egg(project_path)
        # if built, save or update project to db
        if egg:
            built_at = timezone.datetime.fromtimestamp(os.path.getmtime(join(project_path, egg)),
                                                       tz=pytz.timezone(TIME_ZONE))
            if not Project.objects.filter(name=project_name):
                Project(name=project_name, built_at=built_at, egg=egg).save()
                model = Project.objects.get(name=project_name)
            else:
                model = Project.objects.get(name=project_name)
                model.built_at = built_at
                model.egg = egg
                model.save()
        # if not built, just save project name to db
        else:
            if not Project.objects.filter(name=project_name):
                Project(name=project_name).save()
            model = Project.objects.get(name=project_name)
        # transfer model to dict then dumps it to json
        data = model_to_dict(model)
        return JsonResponse(data)
    # build operation manually by clicking button
    elif request.method == 'POST':
        data = json.loads(request.body)
        description = data['description']
        build_project(project_name)
        egg = find_egg(project_path)
        # update built_at info
        built_at = timezone.now()
        # if project does not exists in db, create it
        if not Project.objects.filter(name=project_name):
            Project(name=project_name, description=description, built_at=built_at, egg=egg).save()
            model = Project.objects.get(name=project_name)
        # if project exists, update egg, description, built_at info
        else:
            model = Project.objects.get(name=project_name)
            model.built_at = built_at
            model.egg = egg
            model.description = description
            model.save()
        # transfer model to dict then dumps it to json
        data = model_to_dict(model)
        return JsonResponse(data)


def project_generate(request, project_name):
    """
    generate code of project
    :param request: Request object
    :param project_name: Project name
    :return: JsonResponse
    """
    if request.method == 'POST':
        # get configuration
        configuration = Project.objects.get(name=project_name).configuration
        configuration = json.loads(configuration)
        
        if not is_valid_name(project_name):
            return JsonResponse({'message': 'Invalid project name'}, status=500)
        # remove original project dir
        project_dir = join(PROJECTS_FOLDER, project_name)
        if exists(project_dir):
            shutil.rmtree(project_dir)
        # generate project
        copytree(join(TEMPLATES_DIR, 'project'), project_dir)
        move(join(PROJECTS_FOLDER, project_name, 'module'), join(project_dir, project_name))
        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tplfile = join(project_dir,
                           string.Template(path).substitute(project_name=project_name))
            vars = {
                'project_name': project_name,
                'items': configuration.get('items'),
            }
            render_templatefile(tplfile, tplfile.rstrip('.tmpl'), **vars)
        # generate spider
        spiders = configuration.get('spiders')
        for spider in spiders:
            source_tpl_file = join(TEMPLATES_DIR, 'spiders', 'crawl.tmpl')
            new_tpl_file = join(PROJECTS_FOLDER, project_name, project_name, 'spiders', 'crawl.tmpl')
            spider_file = "%s.py" % join(PROJECTS_FOLDER, project_name, project_name, 'spiders', spider.get('name'))
            copy(source_tpl_file, new_tpl_file)
            render_templatefile(new_tpl_file, spider_file, spider=spider, project_name=project_name)
        # save generated_at attr
        model = Project.objects.get(name=project_name)
        model.generated_at = timezone.now()
        # clear built_at attr
        model.built_at = None
        model.save()
        # return model
        return JsonResponse(model_to_dict(model))


def project_file_read(request):
    """
    get content of project file
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        path = join(data['path'], data['label'])
        with open(path, 'r') as f:
            return HttpResponse(f.read())


def project_file_update(request):
    """
    update project file
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        path = join(data['path'], data['label'])
        code = data['code']
        with open(path, 'w') as f:
            f.write(code)
            return JsonResponse({'result': '1'})


def project_file_create(request):
    """
    create project file
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        path = join(data['path'], data['name'])
        open(path, 'w').close()
        return JsonResponse({'result': '1'})


def project_file_delete(request):
    """
    delete project file
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        path = join(data['path'], data['label'])
        result = os.remove(path)
        return JsonResponse({'result': result})


def project_file_rename(request):
    """
    rename file name
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        pre = join(data['path'], data['pre'])
        new = join(data['path'], data['new'])
        os.rename(pre, new)
        return JsonResponse({'result': '1'})


def job_list(request, id, project):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.list_jobs(project)
        jobs = []
        statuses = ['pending', 'running', 'finished']
        for status in statuses:
            for job in result.get(status):
                job['status'] = status
                jobs.append(job)
        return HttpResponse(json.dumps(jobs, cls=JSONEncoder))


def job_log(request, id, project, spider, job):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        url = log_url(client.ip, client.port, project, spider, job)
        try:
            response = requests.get(url, timeout=5, headers={
                'Range': 'bytes=-1000'
            })
            if response.status_code == 404:
                return HttpResponse('日志不存在')
            text = response.text
            return HttpResponse(text)
        except requests.ConnectionError:
            return HttpResponse('日志加载失败')


def job_cancel(request, id, project, job):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.cancel(project, job)
        return HttpResponse(json.dumps(result, cls=JSONEncoder))


def monitor_db_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        type = data['type']
        if type == 'MongoDB':
            client = pymongo.MongoClient(url)
            dbs = client.database_names()
            return HttpResponse(json.dumps(dbs, cls=JSONEncoder))


def monitor_collection_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        db = data['db']
        type = data['type']
        if type == 'MongoDB':
            client = pymongo.MongoClient(url)
            db = client[db]
            collections = db.collection_names()
            return HttpResponse(json.dumps(collections, cls=JSONEncoder))


def monitor_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = data['form']
        data['configuration'] = json.dumps(data['configuration'])
        monitor = Monitor.objects.create(**data)
        return HttpResponse(json.dumps(model_to_dict(monitor, cls=JSONEncoder)))

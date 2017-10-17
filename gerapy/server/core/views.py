import json
import os
import requests
import shutil
import time
import pytz
import pymongo
import string
from django.shortcuts import render
from gerapy.server.core.build import build_project, find_egg
from gerapy.server.core.utils import IGNORES, is_valid_name, copytree, TEMPLATES_DIR, TEMPLATES_TO_RENDER, \
    render_templatefile, get_traceback
from gerapy.cmd.init import PROJECTS_FOLDER
from gerapy.server.core.utils import scrapyd_url, log_url, get_tree
from gerapy.server.core.models import Client, Project, Deploy, Monitor
from django.core.serializers import serialize
from django.http import HttpResponse
from django.forms.models import model_to_dict
from scrapyd_api import ScrapydAPI
from requests.exceptions import ConnectionError
from os.path import join, exists
from shutil import move, copy
from gerapy.server.server.settings import TIME_ZONE
from django.utils import timezone
from gerapy.server.core.response import JsonResponse


def index(request):
    return render(request, 'index.html')


def index_status(request):
    """
    index statistics
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'GET':
        clients = Client.objects.all()
        data = {
            'success': 0,
            'error': 0,
            'project': 0,
        }
        # clients info
        for client in clients:
            try:
                requests.get(scrapyd_url(client.ip, client.port), timeout=1)
                data['success'] += 1
            except ConnectionError:
                data['error'] += 1
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        files = os.listdir(path)
        # projects info
        for file in files:
            if os.path.isdir(join(path, file)) and not file in IGNORES:
                data['project'] += 1
        return JsonResponse(data)


def client_index(request):
    """
    get client list
    :param request: Request object
    :return: Client list
    """
    return HttpResponse(serialize('json', Client.objects.order_by('-id')))


def client_info(request, client_id):
    """
    get client info
    :param request: Request object
    :param id: Client id
    :return: JsonResponse
    """
    if request.method == 'GET':
        return JsonResponse(model_to_dict(Client.objects.get(id=client_id)))


def client_status(request, client_id):
    """
    get client status
    :param request: Request object
    :param client_id: Client id
    :return: JsonResponse
    """
    if request.method == 'GET':
        # get client object
        client = Client.objects.get(id=client_id)
        try:
            requests.get(scrapyd_url(client.ip, client.port), timeout=3)
            return JsonResponse({'result': '1'})
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


def client_update(request, client_id):
    """
    update client info
    :param request: Request object
    :param client_id: Client id
    :return: JsonResponse
    """
    if request.method == 'POST':
        client = Client.objects.filter(id=client_id)
        data = json.loads(request.body)
        client.update(**data)
        return JsonResponse(model_to_dict(Client.objects.get(id=client_id)))


def client_create(request):
    """
    create a client
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        client = Client.objects.create(**data)
        return JsonResponse(model_to_dict(client))


def client_remove(request, client_id):
    """
    remove a client
    :param request: Request object
    :param client_id: Client id
    :return: JsonResponse
    """
    if request.method == 'POST':
        Client.objects.filter(id=client_id).delete()
        return JsonResponse({'result': '1'})


def spider_list(request, client_id, project_name):
    """
    get spider list from one client
    :param request: Request Object
    :param client_id: Client id
    :param project_name: Project name
    :return: JsonResponse
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        try:
            spiders = scrapyd.list_spiders(project_name)
            spiders = [{'name': spider, 'id': index + 1} for index, spider in enumerate(spiders)]
            return JsonResponse(spiders)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


def spider_start(request, client_id, project_name, spider_name):
    """
    start a spider
    :param request: Request object
    :param client_id: Client id
    :param project_name: Project name
    :param spider_name: Spider name
    :return: JsonResponse
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        try:
            job = scrapyd.schedule(project_name, spider_name)
            return JsonResponse({'job': job})
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


def project_list(request, client_id):
    """
    project deployed list on one client
    :param request: Request object
    :param client_id: Client id
    :return: JsonResponse
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        try:
            projects = scrapyd.list_projects()
            return JsonResponse(projects)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


def project_index(request):
    """
    project index list
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'GET':
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        files = os.listdir(path)
        project_list = []
        for file in files:
            if os.path.isdir(join(path, file)) and not file in IGNORES:
                project_list.append({'name': file})
        return JsonResponse(project_list)


def project_configure(request, project_name):
    """
    get or update configuration
    :param request: Request object
    :param project_name: Project name
    :return: JsonResponse
    """
    # get configuration
    if request.method == 'GET':
        project = Project.objects.get(name=project_name)
        project = model_to_dict(project)
        project['configuration'] = json.loads(project['configuration']) if project['configuration'] else None
        return JsonResponse(project)
    # update configuration
    elif request.method == 'POST':
        project = Project.objects.filter(name=project_name)
        data = json.loads(request.body)
        configuration = json.dumps(data.get('configuration'))
        project.update(**{'configuration': configuration})
        project = Project.objects.get(name=project_name)
        project = model_to_dict(project)
        return JsonResponse(project)


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


def project_create(request):
    """
    create a configurable project
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        data['configurable'] = 1
        project, result = Project.objects.update_or_create(**data)
        return JsonResponse(model_to_dict(project))


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
            except ConnectionError:
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


def job_list(request, client_id, project_name):
    """
    get job list of project from one client
    :param request: Request object
    :param client_id: Client id
    :param project_name: Project name
    :return: JsonResponse
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        try:
            result = scrapyd.list_jobs(project_name)
            jobs = []
            statuses = ['pending', 'running', 'finished']
            for status in statuses:
                for job in result.get(status):
                    job['status'] = status
                    jobs.append(job)
            return JsonResponse(jobs)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


def job_log(request, client_id, project_name, spider_name, job_id):
    """
    get log of jog
    :param request: Request object
    :param client_id: Client id
    :param project_name: Project name
    :param spider_name: Spider name
    :param job_id: Job id
    :return: JsonResponse
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        # get log url
        url = log_url(client.ip, client.port, project_name, spider_name, job_id)
        try:
            # get last 1000 bytes of log
            response = requests.get(url, timeout=5, headers={
                'Range': 'bytes=-1000'
            })
            # log not found
            if response.status_code == 404:
                return JsonResponse({'message': 'Log Not Found'}, status=404)
            text = response.text
            return HttpResponse(text)
        except requests.ConnectionError:
            return JsonResponse({'message': 'Load Log Error'}, status=500)


def job_cancel(request, client_id, project_name, job_id):
    """
    cancel a job
    :param request: Request object
    :param client_id: Client id
    :param project_name: Project name
    :param job_id: Job id
    :return: JsonResponse
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        try:
            scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
            result = scrapyd.cancel(project_name, job_id)
            return JsonResponse(result)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'})


def monitor_db_list(request):
    """
    get monitor db list
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        type = data['type']
        if type == 'MongoDB':
            client = pymongo.MongoClient(url)
            dbs = client.database_names()
            return JsonResponse(dbs)


def monitor_collection_list(request):
    """
    get monitor collection list
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        db = data['db']
        type = data['type']
        if type == 'MongoDB':
            client = pymongo.MongoClient(url)
            db = client[db]
            collections = db.collection_names()
            return JsonResponse(collections)


def monitor_create(request):
    """
    create a monitor
    :param request: Request object
    :return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        data = data['form']
        data['configuration'] = json.dumps(data['configuration'])
        monitor = Monitor.objects.create(**data)
        return JsonResponse(model_to_dict(monitor))

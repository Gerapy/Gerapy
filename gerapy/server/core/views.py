import json
import os
import requests
import shutil
import time
from django.shortcuts import render

from gerapy.server.core.build import build_project, find_egg
from gerapy.server.core.utils import IGNORES
from gerapy.cmd.init import PROJECTS_FOLDER
from gerapy.server.core.utils import scrapyd_url, log_url, get_tree, merge
from gerapy.server.core.models import Client, Project
from django.core.serializers import serialize
from django.http import HttpResponse
from django.forms.models import model_to_dict
from scrapyd_api import ScrapydAPI


def index(request):
    return render(request, 'index.html')


def client_index(request):
    return HttpResponse(serialize('json', Client.objects.order_by('-id')))


def client_show(request, id):
    if request.method == 'GET':
        return HttpResponse(json.dumps(model_to_dict(Client.objects.get(id=id))))


def client_update(request, id):
    if request.method == 'POST':
        client = Client.objects.filter(id=id)
        data = json.loads(request.body)
        client.update(**data)
        return HttpResponse(json.dumps(model_to_dict(Client.objects.get(id=id))))


def list_projects(request, id):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        projects = scrapyd.list_projects()
        return HttpResponse(json.dumps(projects))


def list_spiders(request, id, project):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        spiders = scrapyd.list_spiders(project)
        spiders = [{'name': spider, 'id': index + 1} for index, spider in enumerate(spiders)]
        return HttpResponse(json.dumps(spiders))


def start_spider(request, id, project, spider):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.schedule(project, spider)
        return HttpResponse(json.dumps({'job': result}))


def list_jobs(request, id, project):
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
        return HttpResponse(json.dumps(jobs))


def job_log(request, id, project, spider, job):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        url = log_url(client.ip, client.port, project, spider, job)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                text = response.text
                return HttpResponse(text[-5000:-1])
            if response.status_code == 404:
                return HttpResponse('日志不存在')
        except requests.ConnectionError:
            return HttpResponse('日志加载失败')


def cancel_job(request, id, project, job):
    if request.method == 'GET':
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.cancel(project, job)
        return HttpResponse(json.dumps(result))


def project_index(request):
    if request.method == 'GET':
        path = os.path.abspath(merge(os.getcwd(), PROJECTS_FOLDER))
        files = os.listdir(path)
        project_list = []
        for file in files:
            if os.path.isdir(merge(path, file)) and not file in IGNORES:
                project_list.append({'name': file})
        return HttpResponse(json.dumps(project_list))


def project_tree(request, name):
    if request.method == 'GET':
        path = os.path.abspath(merge(os.getcwd(), PROJECTS_FOLDER))
        tree = get_tree(merge(path, name))
        return HttpResponse(json.dumps(tree))


def project_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        path = merge(data['path'], data['label'])
        with open(path, 'r') as f:
            return HttpResponse(f.read())


def project_file_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        path = merge(data['path'], data['label'])
        code = data['code']
        with open(path, 'w') as f:
            f.write(code)
            return HttpResponse(json.dumps('1'))


def project_file_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        path = merge(data['path'], data['label'])
        result = os.remove(path)
        return HttpResponse(json.dumps(result))


def project_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        path = merge(os.path.abspath(os.getcwd()), PROJECTS_FOLDER)
        project = data['name']
        shutil.rmtree(merge(path, project))
        return HttpResponse(json.dumps('1'))


def project_versions(request, id, project):
    if request.method == 'GET':
        print(project)
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        versions = scrapyd.list_versions(project)
        print(versions)
        if len(versions) > 0:
            version = versions[-1]
            localtime = time.localtime(int(version))
            version = time.strftime('%Y-%m-%d %H:%M:%S', localtime)
            return HttpResponse(json.dumps(version))
        return HttpResponse(None)


def project_deploy(request, id, project):
    if request.method == 'GET':
        print(id, project)
        egg = build_project(project)
        print(egg)
        egg_file = open(egg, 'rb')
        deploy_version = time.time()
        print(deploy_version)
        client = Client.objects.get(id=id)
        scrapyd = ScrapydAPI(scrapyd_url(client.ip, client.port))
        result = scrapyd.add_version(project, int(deploy_version), egg_file.read())
        print(result)
        return HttpResponse(result)


def project_build(request, project):
    if request.method == 'GET':
        print(project)
        path = os.path.abspath(merge(os.getcwd(), PROJECTS_FOLDER))
        project_path = merge(path, project)
        egg = find_egg(project_path)
        if egg:
            built_at = os.path.getmtime(merge(project_path, egg))
            print(built_at)
            if not Project.objects.filter(name=project):
                Project(name=project, built_at=built_at).save()
            else:
                model = Project.objects.get(name=project)
                model.built_at = built_at
                model.save()
                print(model)
            dict = model_to_dict(model)
            print(dict)
            localtime = time.localtime(int(built_at))
            dict['built_at'] = time.strftime('%Y-%m-%d %H:%M:%S', localtime)
            return HttpResponse(json.dumps(dict))
        else:
            return HttpResponse(json.dumps({'name': project}))
    
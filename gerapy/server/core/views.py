import re
from pathlib import Path
from urllib.parse import unquote
import base64
import json
import os
import requests
import time
import pytz
import pymongo
from shutil import rmtree
from requests.exceptions import ConnectionError
from os.path import join, exists
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from subprocess import Popen, PIPE
from gerapy import get_logger
from gerapy.server.core.response import JsonResponse
from gerapy.cmd.init import PROJECTS_FOLDER
from gerapy.server.server.settings import TIME_ZONE
from gerapy.server.core.models import Client, Project, Deploy, Monitor, Task
from gerapy.server.core.build import build_project, find_egg
from gerapy.server.core.utils import IGNORES, is_in_curdir, scrapyd_url, log_url, get_tree, get_scrapyd, process_html, bytes2str, \
    clients_of_task, get_job_id, log_exception
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from django.core.files.storage import FileSystemStorage
import zipfile

logger = get_logger(__name__)


@log_exception()
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def index(request):
    """
    render index page
    :param request: request object
    :return: page
    """
    return render(request, 'index.html')


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index_status(request):
    """
    index statistics
    :param request: request object
    :return: json
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


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_index(request):
    """
    get client list
    :param request: request object
    :return: client list
    """
    return HttpResponse(serialize('json', Client.objects.order_by('-id')))


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_info(request, client_id):
    """
    get client info
    :param request: request object
    :param id: client id
    :return: json
    """
    if request.method == 'GET':
        return JsonResponse(model_to_dict(Client.objects.get(id=client_id)))


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_status(request, client_id):
    """
    get client status
    :param request: request object
    :param client_id: client id
    :return: json
    """
    if request.method == 'GET':
        # get client object
        client = Client.objects.get(id=client_id)
        requests.get(scrapyd_url(client.ip, client.port), timeout=3)
        return JsonResponse({'result': '1'})


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def client_update(request, client_id):
    """
    update client info
    :param request: request object
    :param client_id: client id
    :return: json
    """
    if request.method == 'POST':
        client = Client.objects.filter(id=client_id)
        data = json.loads(request.body)
        client.update(**data)
        return JsonResponse(model_to_dict(Client.objects.get(id=client_id)))


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def client_create(request):
    """
    create a client
    :param request: request object
    :return: json
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        client = Client.objects.create(**data)
        return JsonResponse(model_to_dict(client))


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def client_remove(request, client_id):
    """
    remove a client
    :param request: request object
    :param client_id: client id
    :return: json
    """
    if request.method == 'POST':
        client = Client.objects.get(id=client_id)
        # delete deploy
        Deploy.objects.filter(client=client).delete()
        # delete client
        Client.objects.filter(id=client_id).delete()
        return JsonResponse({'result': '1'})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spider_list(request, client_id, project_name):
    """
    get spider list from one client
    :param request: request Object
    :param client_id: client id
    :param project_name: project name
    :return: json
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        spiders = scrapyd.list_spiders(project_name)
        spiders = [{'name': spider, 'id': index + 1}
                   for index, spider in enumerate(spiders)]
        return JsonResponse(spiders)


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spider_start(request, client_id, project_name, spider_name):
    """
    start a spider
    :param request: request object
    :param client_id: client id
    :param project_name: project name
    :param spider_name: spider name
    :return: json
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        job = scrapyd.schedule(project_name, spider_name)
        return JsonResponse({'job': job})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_list(request, client_id):
    """
    project deployed list on one client
    :param request: request object
    :param client_id: client id
    :return: json
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        projects = scrapyd.list_projects()
        return JsonResponse(projects)


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_index(request):
    """
    project index list
    :param request: request object
    :return: json
    """
    if request.method == 'GET':
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        files = os.listdir(path)
        project_list = []
        for file in files:
            if os.path.isdir(join(path, file)) and not file in IGNORES:
                project_list.append({'name': file})
        return JsonResponse(project_list)


@log_exception()
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def project_configure(request, project_name):
    """
    get configuration
    :param request: request object
    :param project_name: project name
    :return: json
    """
    # get configuration
    if request.method == 'GET':
        project = Project.objects.get(name=project_name)
        project = model_to_dict(project)
        project['configuration'] = json.loads(
            project['configuration']) if project['configuration'] else None
        return JsonResponse(project)

    # update configuration
    elif request.method == 'POST':
        project = Project.objects.filter(name=project_name)
        data = json.loads(request.body)
        configuration = json.dumps(
            data.get('configuration'), ensure_ascii=False)
        project.update(**{'configuration': configuration})
        # for safe protection
        project_name = re.sub(
            '[\s\!\@\#\$\;\&\*\~\"\'\{\}\]\[\-\+\%\^]+', '', project_name)
        # execute generate cmd
        cmd = ['gerapy', 'generate', project_name]
        p = Popen(cmd, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = bytes2str(p.stdout.read()), bytes2str(p.stderr.read())

        if not stderr:
            return JsonResponse({'status': '1'})
        else:
            return JsonResponse({'status': '0', 'message': stderr})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_tree(request, project_name):
    """
    get file tree of project
    :param request: request object
    :param project_name: project name
    :return: json of tree
    """
    if request.method == 'GET':
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        # get tree data
        tree = get_tree(join(path, project_name))
        return JsonResponse(tree)


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_create(request):
    """
    create a configurable project
    :param request: request object
    :return: json
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        data['configurable'] = 1
        project, result = Project.objects.update_or_create(**data)
        # generate a single project folder
        path = join(os.path.abspath(
            join(os.getcwd(), PROJECTS_FOLDER)), data['name'])
        os.mkdir(path)
        return JsonResponse(model_to_dict(project))


@log_exception()
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def project_upload(request):
    """
    upload project
    :param request: request object
    :return: json
    """
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = file.name
        fs = FileSystemStorage(PROJECTS_FOLDER)
        zip_file_name = fs.save(file_name, file)
        logger.debug('zip file name %s', zip_file_name)
        # extract zip file
        with zipfile.ZipFile(join(PROJECTS_FOLDER, zip_file_name), 'r') as zip_ref:
            zip_ref.extractall(PROJECTS_FOLDER)
        logger.debug('extracted files to %s', PROJECTS_FOLDER)
        return JsonResponse({'status': True})


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_clone(request):
    """
    clone project from github
    :param request: request object
    :return: json
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        address = data.get('address')
        if not address.startswith('http'):
            return JsonResponse({'status': False})
        address = address + '.git' if not address.endswith('.git') else address
        cmd = ['git', 'clone', address, join(PROJECTS_FOLDER, Path(address).stem)]
        logger.debug('clone cmd %s', cmd)
        p = Popen(cmd, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = bytes2str(p.stdout.read()), bytes2str(p.stderr.read())
        logger.debug('clone run result %s', stdout)
        if stderr:
            logger.error(stderr)
        return JsonResponse({'status': True}) if not stderr else JsonResponse({'status': False})


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_remove(request, project_name):
    """
    remove project from disk and db
    :param request: request object
    :param project_name: project name
    :return: result of remove
    """
    if request.method == 'POST':
        # delete deployments
        project = Project.objects.get(name=project_name)
        Deploy.objects.filter(project=project).delete()
        # delete project
        result = Project.objects.filter(name=project_name).delete()
        # get project path
        path = join(os.path.abspath(os.getcwd()), PROJECTS_FOLDER)
        project_path = join(path, project_name)
        # delete project file tree
        if exists(project_path):
            rmtree(project_path)
        return JsonResponse({'result': result})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_version(request, client_id, project_name):
    """
    get project deploy version
    :param request: request object
    :param client_id: client id
    :param project_name: project name
    :return: deploy version of project
    """
    if request.method == 'GET':
        # get client and project model
        client = Client.objects.get(id=client_id)
        project = Project.objects.get(name=project_name)
        scrapyd = get_scrapyd(client)
        # if deploy info exists in db, return it
        if Deploy.objects.filter(client=client, project=project):
            deploy = Deploy.objects.get(client=client, project=project)
        # if deploy info does not exists in db, create deploy info
        else:
            try:
                versions = scrapyd.list_versions(project_name)
            except ConnectionError:
                logger.exception('cannot connect to scrapyd', exc_info=True)
                return JsonResponse({'message': 'Connect Error'}, status=500)
            if len(versions) > 0:
                version = versions[-1]
                deployed_at = timezone.datetime.fromtimestamp(
                    int(version), tz=pytz.timezone(TIME_ZONE))
            else:
                deployed_at = None
            deploy, result = Deploy.objects.update_or_create(
                client=client, project=project, deployed_at=deployed_at)
        # return deploy json info
        return JsonResponse(model_to_dict(deploy))


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_deploy(request, client_id, project_name):
    """
    deploy project operation
    :param request: request object
    :param client_id: client id
    :param project_name: project name
    :return: json of deploy result
    """
    if request.method == 'POST':
        # get project folder
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        project_path = join(path, project_name)
        # find egg file
        egg = find_egg(project_path)
        if not egg:
            return JsonResponse({'message': 'egg not found'}, status=500)
        egg_file = open(join(project_path, egg), 'rb')
        # get client and project model
        client = Client.objects.get(id=client_id)
        project = Project.objects.get(name=project_name)
        # execute deploy operation
        scrapyd = get_scrapyd(client)
        scrapyd.add_version(project_name, int(time.time()), egg_file.read())
        # update deploy info
        deployed_at = timezone.now()
        Deploy.objects.filter(client=client, project=project).delete()
        deploy, result = Deploy.objects.update_or_create(client=client, project=project, deployed_at=deployed_at,
                                                         description=project.description)
        return JsonResponse(model_to_dict(deploy))


@log_exception()
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def project_build(request, project_name):
    """
    get build info or execute build operation
    :param request: request object
    :param project_name: project name
    :return: json
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
        if not egg:
            return JsonResponse({'message': 'egg not found'}, status=500)
        # update built_at info
        built_at = timezone.now()
        # if project does not exists in db, create it
        if not Project.objects.filter(name=project_name):
            Project(name=project_name, description=description,
                    built_at=built_at, egg=egg).save()
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


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_parse(request, project_name):
    """
    parse project
    :param request: request object
    :param project_name: project name
    :return: requests, items, response
    """
    if request.method == 'POST':
        project_path = join(PROJECTS_FOLDER, project_name)
        data = json.loads(request.body)
        logger.debug('post data %s', data)
        spider_name = data.get('spider')
        args = {
            'start': data.get('start', False),
            'method': data.get('method', 'GET'),
            'url': data.get('url'),
            'callback': data.get('callback'),
            'cookies': "'" + json.dumps(data.get('cookies', {}), ensure_ascii=False) + "'",
            'headers': "'" + json.dumps(data.get('headers', {}), ensure_ascii=False) + "'",
            'meta': "'" + json.dumps(data.get('meta', {}), ensure_ascii=False) + "'",
            'dont_filter': data.get('dont_filter', False),
            'priority': data.get('priority', 0),
        }
        # set request body
        body = data.get('body', '')
        if args.get('method').lower() != 'get':
            args['body'] = "'" + json.dumps(body, ensure_ascii=False) + "'"

        args_array = []
        for arg, value in args.items():
            args_array.append(f'--{arg}')
            args_array.append(f'{value}')
        cmd = ['gerapy', 'parse'] + args_array + [project_path] + [spider_name]
        logger.debug('parse cmd %s', cmd)
        p = Popen(cmd, shell=False, stdin=PIPE,
                         stdout=PIPE, stderr=PIPE, close_fds=True)
        stdout, stderr = bytes2str(p.stdout.read()), bytes2str(p.stderr.read())
        logger.debug('stdout %s, stderr %s', stdout, stderr)
        if not stderr:
            return JsonResponse({'status': True, 'result': json.loads(stdout)})
        else:
            return JsonResponse({'status': False, 'message': stderr})


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_file_read(request):
    """
    get content of project file
    :param request: request object
    :return: file content
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        path = join(data['path'], data['label'])
        if not is_in_curdir(path):
            return JsonResponse({'result': '0'})
        # binary file
        with open(path, 'rb') as f:
            return HttpResponse(f.read().decode('utf-8'))


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_file_update(request):
    """
    update project file
    :param request: request object
    :return: result of update
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        path = join(data['path'], data['label'])
        code = data['code']
        if not is_in_curdir(path):
            return JsonResponse({'result': '0'})
        with open(path, 'w', encoding='utf-8') as f:
            f.write(code)
            return JsonResponse({'result': '1'})


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_file_create(request):
    """
    create project file
    :param request: request object
    :return: result of create
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        path = join(data['path'], data['name'])
        if not is_in_curdir(path):
            return JsonResponse({'result': '0'})
        open(path, 'w', encoding='utf-8').close()
        return JsonResponse({'result': '1'})


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_file_delete(request):
    """
    delete project file
    :param request: request object
    :return: result of delete
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        path = join(data['path'], data['label'])
        if not is_in_curdir(path):
            return JsonResponse({'result': '0'})
        result = os.remove(path)
        return JsonResponse({'result': result})


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_file_rename(request):
    """
    rename file name
    :param request: request object
    :return: result of rename
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        pre = join(data['path'], data['pre'])
        new = join(data['path'], data['new'])
        if not is_in_curdir(pre) or not is_in_curdir(new):
            return JsonResponse({'result': '0'})
        os.rename(pre, new)
        return JsonResponse({'result': '1'})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_list(request, client_id, project_name):
    """
    get job list of project from one client
    :param request: request object
    :param client_id: client id
    :param project_name: project name
    :return: list of jobs
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        result = scrapyd.list_jobs(project_name)
        jobs = []
        statuses = ['pending', 'running', 'finished']
        for status in statuses:
            for job in result.get(status):
                job['status'] = status
                jobs.append(job)
        return JsonResponse(jobs)


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_log(request, client_id, project_name, spider_name, job_id):
    """
    get log of jog
    :param request: request object
    :param client_id: client id
    :param project_name: project name
    :param spider_name: spider name
    :param job_id: job id
    :return: log of job
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        # get log url
        url = log_url(client.ip, client.port,
                      project_name, spider_name, job_id)
        # get last 1000 bytes of log
        response = requests.get(url, timeout=5, headers={
            'Range': 'bytes=-1000'
        }, auth=(client.username, client.password) if client.auth else None)
        # Get encoding
        encoding = response.apparent_encoding
        # log not found
        if response.status_code == 404:
            return JsonResponse({'message': 'Log Not Found'}, status=404)
        # bytes to string
        text = response.content.decode(encoding, errors='replace')
        return HttpResponse(text)


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_cancel(request, client_id, project_name, job_id):
    """
    cancel a job
    :param request: request object
    :param client_id: client id
    :param project_name: project name
    :param job_id: job id
    :return: json of cancel
    """
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        result = scrapyd.cancel(project_name, job_id)
        return JsonResponse(result)


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def del_version(request, client_id, project, version):
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        result = scrapyd.delete_version(project=project, version=version)
        return JsonResponse(result)


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def del_project(request, client_id, project):
    if request.method == 'GET':
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        result = scrapyd.delete_project(project=project)
        return JsonResponse(result)


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def monitor_db_list(request):
    """
    get monitor db list
    :param request: request object
    :return: json of db list
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        type = data['type']
        if type == 'MongoDB':
            client = pymongo.MongoClient(url)
            dbs = client.list_database_names()
            return JsonResponse(dbs)


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def monitor_collection_list(request):
    """
    get monitor collection list
    :param request: request object
    :return: json of collection list
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


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def monitor_create(request):
    """
    create a monitor
    :param request: request object
    :return: json of create
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        data = data['form']
        data['configuration'] = json.dumps(
            data['configuration'], ensure_ascii=False)
        monitor = Monitor.objects.create(**data)
        return JsonResponse(model_to_dict(monitor))


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create(request):
    """
    add task
    :param request: request object
    :return: Bool
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(clients=json.dumps(data.get('clients'), ensure_ascii=False),
                                   project=data.get('project'),
                                   name=data.get('name'),
                                   spider=data.get('spider'),
                                   trigger=data.get('trigger'),
                                   configuration=json.dumps(
                                       data.get('configuration'), ensure_ascii=False),
                                   modified=1)
        return JsonResponse({'result': '1', 'data': model_to_dict(task)})


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_update(request, task_id):
    """
    update task info
    :param request: request object
    :param task_id: task id
    :return: json
    """
    if request.method == 'POST':
        task = Task.objects.filter(id=task_id)
        data = json.loads(request.body)
        data['clients'] = json.dumps(data.get('clients'), ensure_ascii=False)
        data['configuration'] = json.dumps(
            data.get('configuration'), ensure_ascii=False)
        data['modified'] = 1
        task.update(**data)
        return JsonResponse(model_to_dict(Task.objects.get(id=task_id)))


@log_exception()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_remove(request, task_id):
    """
    remove task by task_id
    :param request:
    :return:
    """
    if request.method == 'POST':
        # delete job from DjangoJob
        task = Task.objects.get(id=task_id)
        clients = clients_of_task(task)
        for client in clients:
            job_id = get_job_id(client, task)
            DjangoJob.objects.filter(id=job_id).delete()
        # delete task
        Task.objects.filter(id=task_id).delete()
        return JsonResponse({'result': '1'})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_info(request, task_id):
    """
    get task info
    :param request: request object
    :param task_id: task id
    :return: json
    """
    if request.method == 'GET':
        task = Task.objects.get(id=task_id)
        data = model_to_dict(task)
        data['clients'] = json.loads(data.get('clients'))
        data['configuration'] = json.loads(data.get('configuration'))
        return JsonResponse({'data': data})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_index(request):
    """
    get all tasks
    :param request:
    :return:
    """
    if request.method == 'GET':
        tasks = Task.objects.values()
        return JsonResponse({'result': '1', 'data': tasks})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_status(request, task_id):
    """
    get task status info
    :param request: request object
    :param task_id: task id
    :return:
    """
    if request.method == 'GET':
        result = []
        task = Task.objects.get(id=task_id)
        clients = clients_of_task(task)
        for client in clients:
            job_id = get_job_id(client, task)
            jobs = DjangoJob.objects.filter(id=job_id)
            logger.debug('jobs from djangojob %s', jobs)
            # if job does not exist, for date mode exceed time
            if not jobs:
                continue
            job = DjangoJob.objects.get(id=job_id)
            executions = serialize(
                'json', DjangoJobExecution.objects.filter(job=job))
            result.append({
                'client': model_to_dict(client),
                'next': job.next_run_time,
                'executions': json.loads(executions)
            })
        return JsonResponse({'data': result})


@log_exception()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def render_html(request):
    """
    render html with url
    :param request:
    :return:
    """
    if request.method == 'GET':
        url = request.GET.get('url')
        url = unquote(base64.b64decode(url).decode('utf-8'))
        js = request.GET.get('js', 0)
        script = request.GET.get('script')
        response = requests.get(url, timeout=5)
        response.encoding = response.apparent_encoding
        html = process_html(response.text)
        return HttpResponse(html)

import json

from django.shortcuts import render
from .models import Client
from django.core.serializers import serialize
from django.http import HttpResponse
from django.forms.models import model_to_dict


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
        data = request.POST.dict()
        client.update(**data)
        return HttpResponse(json.dumps(model_to_dict(Client.objects.get(id=id))))

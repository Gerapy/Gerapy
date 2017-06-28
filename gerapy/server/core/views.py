from django.shortcuts import render
from .models import Client
from django.core.serializers import serialize
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')


def client(requests):
    return HttpResponse(serialize('json', Client.objects.all()))
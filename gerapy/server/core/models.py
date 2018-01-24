# Create your models here.
from django.db.models import Model, CharField, GenericIPAddressField, IntegerField, TextField, DateTimeField, \
    ManyToManyField, ForeignKey, DO_NOTHING


class Client(Model):
    name = CharField(max_length=255, default=None)
    ip = CharField(max_length=255, blank=True, null=True)
    port = IntegerField(default=6800, blank=True, null=True)
    description = TextField(blank=True, null=True)
    auth = IntegerField(default=0, blank=True, null=True)
    username = CharField(max_length=255, blank=True, null=True)
    password = CharField(max_length=255, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Project(Model):
    name = CharField(max_length=255, default=None)
    description = CharField(max_length=255, null=True, blank=True)
    egg = CharField(max_length=255, null=True, blank=True)
    configuration = TextField(blank=True, null=True)
    configurable = IntegerField(default=0, blank=True)
    built_at = DateTimeField(default=None, blank=True, null=True)
    generated_at = DateTimeField(default=None, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    clients = ManyToManyField(Client, through='Deploy', unique=False)


class Deploy(Model):
    client = ForeignKey(Client, unique=False, on_delete=DO_NOTHING)
    project = ForeignKey(Project, unique=False, on_delete=DO_NOTHING)
    description = CharField(max_length=255, blank=True, null=True)
    deployed_at = DateTimeField(default=None, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('client', 'project')


class Monitor(Model):
    name = CharField(max_length=255, default=None)
    description = CharField(max_length=255, default='', blank=True)
    type = CharField(max_length=255, default='', blank=True)
    configuration = TextField(default='', blank=True)
    project = ForeignKey(Project, blank=True, null=True, on_delete=DO_NOTHING)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

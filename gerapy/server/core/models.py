# Create your models here.
from django.db.models import Model, CharField, GenericIPAddressField, IntegerField, TextField, DateTimeField, \
    ManyToManyField, ForeignKey, DO_NOTHING, BooleanField


class Client(Model):
    """
    Scrapyd
    """
    name = CharField(max_length=255, default=None)
    ip = CharField(max_length=255, blank=True, null=True)
    port = IntegerField(default=6800, blank=True, null=True)
    description = TextField(blank=True, null=True)
    auth = IntegerField(default=0, blank=True, null=True)
    username = CharField(max_length=255, blank=True, null=True)
    password = CharField(max_length=255, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        """
        to string
        :return: name
        """
        return self.name


class Project(Model):
    """
    Project Object, for configurable and un-configurable
    """
    name = CharField(max_length=255, default=None)
    description = CharField(max_length=255, null=True, blank=True)
    egg = CharField(max_length=255, null=True, blank=True)
    configuration = TextField(blank=True, null=True)
    configurable = IntegerField(default=0, blank=True)
    built_at = DateTimeField(default=None, blank=True, null=True)
    generated_at = DateTimeField(default=None, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)
    clients = ManyToManyField(Client, through='Deploy', unique=False)
    
    def __str__(self):
        """
        to string
        :return: name
        """
        return self.name


class Deploy(Model):
    """
    Deploy records
    """
    client = ForeignKey(Client, unique=False, on_delete=DO_NOTHING)
    project = ForeignKey(Project, unique=False, on_delete=DO_NOTHING)
    description = CharField(max_length=255, blank=True, null=True)
    deployed_at = DateTimeField(default=None, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        unique_together = ('client', 'project')


class Monitor(Model):
    """
    Monitor configuration
    """
    name = CharField(max_length=255, default=None)
    description = CharField(max_length=255, null=True, blank=True)
    type = CharField(max_length=255, null=True, blank=True)
    configuration = TextField(null=True, blank=True)
    project = ForeignKey(Project, blank=True, null=True, on_delete=DO_NOTHING)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)


class Task(Model):
    """
    Task for scheduler
    """
    clients = TextField(null=True, blank=True)
    project = CharField(max_length=255, null=True, blank=True)
    spider = CharField(max_length=255, null=True, blank=True)
    name = CharField(max_length=255, null=True, blank=True)
    args = TextField(null=True, blank=True)
    description = TextField(null=True, blank=True)
    trigger = CharField(max_length=255, null=True, blank=True)
    configuration = TextField(null=True, blank=True)
    modified = BooleanField(blank=True, default=False)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        """
        to string
        :return: name
        """
        return '_'.join([str(self.name), str(self.project), str(self.spider)])

from django.contrib import admin

# Register your models here.
from gerapy.server.core.models import Client, Project, Monitor


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'port', 'created_at', 'updated_at')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'configurable', 'built_at', 'generated_at')


class MonitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'project', 'created_at', 'updated_at')


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Monitor, MonitorAdmin)

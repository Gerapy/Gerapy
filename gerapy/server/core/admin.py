from django.contrib import admin

# Register your models here.
from gerapy.server.core.models import Client, Project, Monitor

admin.site.site_header = '爬虫后台管理'
admin.site.site_title = '爬虫后台管理'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'port', 'created_at', 'updated_at']
    search_fields = ['name', 'ip']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'configurable', 'built_at', 'generated_at']
    search_fields = ['name']


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'project', 'created_at', 'updated_at']
    search_fields = ('name',)

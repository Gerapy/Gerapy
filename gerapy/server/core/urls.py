from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/client/$', views.client_index, name='client_index'),
    url(r'^api/client/create', views.client_create, name='client_create'),
    url(r'^api/client/(\d+)/$', views.client_show, name='client_show'),
    url(r'^api/client/(\d+)/status', views.client_status, name='client_status'),
    url(r'^api/client/(\d+)/update', views.client_update, name='client_update'),
    url(r'^api/client/(\d+)/remove', views.client_remove, name='client_remove'),
    url(r'^api/client/(\d+)/projects/$', views.list_projects, name='list_projects'),
    url(r'^api/client/(\d+)/project/(\S+)/spiders/$', views.list_spiders, name='list_spiders'),
    url(r'^api/client/(\d+)/project/(\S+)/spider/(\S+)/job/(\S+)/log', views.job_log, name='job_log'),
    url(r'^api/client/(\d+)/project/(\S+)/spider/(\S+)/$', views.start_spider, name='start_spider'),
    url(r'^api/client/(\d+)/project/(\S+)/jobs/$', views.list_jobs, name='list_jobs'),
    url(r'^api/client/(\d+)/project/(\S+)/versions/$', views.project_versions, name='project_versions'),
    url(r'^api/client/(\d+)/project/(\S+)/deploy/$', views.project_deploy, name='project_deploy'),
    url(r'^api/client/(\d+)/project/(\S+)/job/(\S+)/cancel$', views.cancel_job, name='cancel_job'),
    url(r'^api/project/index/$', views.project_index, name='project_index'),
    url(r'^api/project/(\S+)/build', views.project_build, name='project_build'),
    url(r'^api/project/(\S+)/tree', views.project_tree, name='project_tree'),
    url(r'^api/project/(\S+)/remove', views.project_remove, name='project_remove'),
    url(r'^api/project/file/delete', views.project_file_delete, name='project_file_delete'),
    url(r'^api/project/file/update', views.project_file_update, name='project_file_update'),
    url(r'^api/project/file', views.project_file, name='project_file'),
]

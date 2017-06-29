from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/client/$', views.client_index, name='client_index'),
    url(r'^api/client/(\d+)/$', views.client_show, name='client_show'),
    url(r'^api/client/(\d+)/update/$', views.client_update, name='client_update'),
    url(r'^api/client/(\d+)/projects/$', views.list_projects, name='list_projects'),
    url(r'^api/client/(\d+)/project/(\S+)/spiders/$', views.list_spiders, name='list_spiders'),
    url(r'^api/client/(\d+)/project/(\S+)/spider/(\S+)/job/(\S+)/log', views.job_log, name='job_log'),
    url(r'^api/client/(\d+)/project/(\S+)/spider/(\S+)/$', views.start_spider, name='start_spider'),
    url(r'^api/client/(\d+)/project/(\S+)/jobs/$', views.list_jobs, name='list_jobs'),
]

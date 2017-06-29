from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/client/$', views.client_index, name='client_index'),
    url(r'^api/client/(\d+)/$', views.client_show, name='client_show'),
    url(r'^api/client/(\d+)/update$', views.client_update, name='client_update'),
    url(r'^api/client/(\d+)/projects', views.client_projects, name='client_projects'),
    url(r'^api/client/(\d+)/spiders/(\S+)/', views.project_spiders, name='project_spiders'),
]

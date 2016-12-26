from django.conf.urls import include, url
from django.contrib import admin, auth
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.msg_logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^home/$', views.home, name='home')
]

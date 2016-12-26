from django.conf.urls import include, url
from django.contrib import admin, auth
from . import views

app_name = "chief"
urlpatterns = [
    url(r'^$', views.ProjectList.as_view(), name='index'),


    url(r'^projects/$', views.ProjectList.as_view(), name='projects'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectDetails.as_view(), name='project'),
    url(r'^project/create/$', views.ProjectCreate.as_view(), name='project_create'),
    url(r'^project/upd/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='project_upd'),
    url(r'^project/del/(?P<pk>[0-9]+)/$', views.ProjectDelete.as_view(), name='project_del'),


    url(r'^project/(?P<project_pk>[0-9]+)/orders/upd/(?P<order_pk>[0-9]+)/$', views.OrderUpdate.as_view(), name='order_upd'),
    url(r'^orders/del/(?P<pk>[0-9]+)/$', views.OrderDelete.as_view(), name='order_del'),
    url(r'^project/(?P<project_pk>[0-9]+)/orders/create/$', views.OrderCreate.as_view(), name='order_create'),


    url(r'^project/(?P<project_pk>[0-9]+)/orders/fields/$', views.OrderFieldList.as_view(), name='ord_field_list'),
    url(r'^project/(?P<project_pk>[0-9]+)/orders/fields/create/$', views.OrderFieldCreate.as_view(), name='ord_field_create'),
    url(r'^orders/fields/upd/(?P<pk>[0-9]+)/$', views.OrderFieldUpdate.as_view(), name='ord_field_upd'),
    url(r'^orders/fields/del/(?P<pk>[0-9]+)/$', views.OrderFieldDelete.as_view(), name='ord_field_del'),


    url(r'^project/(?P<project_pk>[0-9]+)/invites/$', views.InviteList.as_view(), name='invites'),
    url(r'^invites/del/(?P<pk>[0-9]+)/$', views.InviteDelete.as_view(), name='invite_del'),
    url(r'^invites/create/$', views.InviteCreate.as_view(), name='invite_create'),


    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
]

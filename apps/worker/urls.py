from django.conf.urls import url
from django.contrib.auth import views as auth_views # del
from django.conf.urls import include
from . import views
from metaord import views as meta_views

app_name = "worker"
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^register/$', views.register_operator_form, name='register'),
    url(r'^register_submit/$', views.register_operator_submit, name='register_submit'),

    url(r'^orders/$', views.OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetail.as_view(), name='order'),
    url(r'^orders/upd_status/(?P<pk>[0-9]+)/$', views.OrderUpdate.as_view(), name='order_upd_status'),
]

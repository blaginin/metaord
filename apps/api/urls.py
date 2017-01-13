from django.conf.urls import include, url
from django.contrib import admin, auth
# from api.views import index
from api.views import index, orders

app_name = "api"
urlpatterns = [
    url(r'^$', index.index, name="index"),
    url(r'^order/create/$', orders.create_order, name="create_order"),
    url(r'^order/view/$', orders.view_order, name="view_order"),
]

from django.conf.urls import include, url
from webms import views

app_name = "webms"
urlpatterns = [
    url(r'^$', views.InviteList.as_view(), name="index"),
    url(r'^$', views.InviteList.as_view(), name="invites"),

    url(r'^invites/(?P<pk>[0-9]+)/upd_status/$', views.InviteUpdateStatus.as_view(), name="invite_upd_status"),

    url(r'^register/$', views.RegistrationView.as_view(), name="register"),
]

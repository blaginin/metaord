from django.conf.urls import include, url
from django.contrib import admin, auth
from metaord import settings
from metaord.models import MetaordSettings
from metaord.views import SettingsUpdate


# if settings.DEBUG:
handler404 = 'metaord.views.page_not_found'
handler500 = 'metaord.views.error_view'
handler400 = 'metaord.views.error_view'


urlpatterns = [
    url(r'^', include('front.urls')),
    url(r'^settings/$', SettingsUpdate.as_view(), name='metaord_settings'),
    url(r'^chief/', include('chief.urls')),
    url(r'^webms/', include('webms.urls')),
    url(r'^worker/', include('worker.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^hook/', include('github_hook.urls')),
    url(r'^', include('captainhook.urls')),
)

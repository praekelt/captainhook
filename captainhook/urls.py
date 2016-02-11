from django.conf.urls import patterns, url, include

from captainhook.views import HookView


urlpatterns = patterns('',
    url(r'^hook/(?P<name>[\w-]+)/$', HookView.as_view()),
)

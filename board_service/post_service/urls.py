from django.conf.urls import patterns, url
from post_service.views import post_list, update, detailed, create

urlpatterns = patterns('',
    url(r'^$', post_list),
    url(r'^update/$', update),
    url(r'^detailed/$', detailed),
    url(r'^create/$', create),
)
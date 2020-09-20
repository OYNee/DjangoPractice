from django.conf.urls import patterns, url
from app.views import img_list

urlpatterns = patterns('',
                       url(r'^$', img_list),
                       )

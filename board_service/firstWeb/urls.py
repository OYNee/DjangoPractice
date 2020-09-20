from django.conf.urls import patterns, include, url
from django.contrib import admin
from practice.views import practice_page, practice_api

import post_service

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'firstWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^rest-api/', include('rest_framework.urls')),
    url(r'^rest-swagger/', include('rest_framework_swagger.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # practice view
    url(r'practice/', practice_page),

    #Rest
    #경로가 위의 practice view와 같으면 practice_page가 열림.
    #예를 들어서, url(r'^api/practice/', practice_api.as_view()), 이렇게 하면, r'practice/ 이 경로의 페이지가 열림
    url(r'^api/practice_api/', practice_api.as_view()),

    url(r'board/', include('post_service.urls')),
    url(r'user/', include('user_manager.urls')),
)

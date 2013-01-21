#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('teambuglist.views',
    url(r'action/$', 'bug_action', name='action'),
    url(r'^$', 'bug_list', name='bug_list'),
    url(r'(?P<pid>(\d+))/$', 'bug', name='bug'),

)
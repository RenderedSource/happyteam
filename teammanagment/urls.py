#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

__author__ = 'lehabaev'
urlpatterns = patterns('',
    url(r'^ajax/task-status/$', 'teammanagment.ajax.taskStatus', name='taskStatus'),
    url(r'^$', 'teammanagment.views.sprint_list', name='sprint_list'),
    url(r'^sprint/(?P<pid>(\d+))/$', 'teammanagment.views.sprint_tasks', name='sprint_list'),
    url(r'^task/(?P<pid>(\d+))/$', 'teammanagment.views.task', name='task'),
    url(r'^day/$', 'teammanagment.views.dayTask', name='dayTask'),
    url(r'^task/$', 'teammanagment.views.taskPrice', name='taskPrice'),
)
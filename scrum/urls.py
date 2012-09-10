#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

__author__ = 'lehabaev'

urlpatterns = patterns('',
    url('^$', 'scrum.views.story_desc',name='story_desc'),
)
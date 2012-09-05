#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

__author__ = 'lehabaev'
urlpatterns = patterns('',
    url(r'^$', 'importantnews.views.archiveNews', name='archive_news'),
    url(r'add/$', 'importantnews.views.addNews', name='add_news'),
    url(r'edit/(?P<pid>(\d+))/$', 'importantnews.views.editNews', name='edit_news'),
    url(r'unread/$', 'importantnews.views.unreadNews', name='unread_news'),
    url(r'(?P<pid>(\d+))/$', 'importantnews.views.readNews', name='read_news'),

)
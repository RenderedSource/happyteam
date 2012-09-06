#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'teamevents.views.calendar',name='calendar'),
    url(r'json$', 'teamevents.views.calendar_data',name='calendar_data'),
    )
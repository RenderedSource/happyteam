#-*- coding: utf-8 -*-

#TeamChat
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('^','teamchat.views.TeamChat', name='group_chat')
)
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mergemaster.views.merge_list'),
    url(r'merge-details/(?P<merge_id>\d+)/$', 'mergemaster.views.merge_details'),
    url(r'add-merge-request/$', 'mergemaster.views.add_merge_request'),
    url(r'add-merge-action/$', 'mergemaster.views.add_merge_action'),
    url(r'add-action-comment/$', 'mergemaster.views.add_action_comment'),
)
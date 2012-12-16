#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<selected_merge_id>\d+)?$', 'mergemaster.views.merge_list'),
    url(r'merge-details/(?P<merge_id>\d+)/$', 'mergemaster.views.merge_details'),
    url(r'add-merge-request/$', 'mergemaster.views.add_merge_request'),
    url(r'update-merge-request/(?P<merge_id>\d+)/$', 'mergemaster.views.update_merge_request', name='update-merge-request'),
    url(r'add-action-comment/$', 'mergemaster.views.add_action_comment'),
    url(r'diff:(?P<from_branch>[a-zA-Z0-9_/-]+):(?P<to_branch>[a-zA-Z0-9_/-]+)$', 'mergemaster.views.diff', name='diff'),
)
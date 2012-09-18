#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mergemaster.views.merge_list'),
    url(r'merge-details/(?P<merge_id>\d+)/$', 'mergemaster.views.merge_details'),
    url(r'add-merge-request/$', 'mergemaster.views.add_merge_request'),
    url(r'update-merge-request/(?P<merge_id>\d+)/$', 'mergemaster.views.update_merge_request', name='update-merge-request'),
    url(r'add-action-comment/$', 'mergemaster.views.add_action_comment'),
)
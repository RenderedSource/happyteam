#-*- coding: utf-8 -*-
from django.contrib import admin
from mergemaster.models import *


class MergeMasterAdmin(admin.ModelAdmin):
  list_display = ['user','enabled']
admin.site.register(MergeMaster, MergeMasterAdmin)

class MergeRequestAdmin(admin.ModelAdmin):
  list_display = ['branch','date_created']
admin.site.register(MergeRequest, MergeRequestAdmin)

class MergeRequestActionAdmin(admin.ModelAdmin):
    pass
admin.site.register(MergeRequestAction, MergeRequestActionAdmin)

#class MergeCommentAdmin(admin.ModelAdmin):
#  pass
#admin.site.register(MergeComment, MergeCommentAdmin)

class MergeNotificationAdmin(admin.ModelAdmin):
  list_display = ['message','user']
admin.site.register(MergeNotification, MergeNotificationAdmin)

#class MergeStatsAdmin(admin.ModelAdmin):
#  pass
#admin.site.register(MergeStats, MergeStatsAdmin)

class JabberMessageAdmin(admin.ModelAdmin):
  pass
admin.site.register(JabberMessage, JabberMessageAdmin)
#-*- coding: utf-8 -*-
from django.contrib import admin
from mergemaster.models import *


class MergeMastersAdmin(admin.ModelAdmin):
  list_display = ['user','status']
admin.site.register(MergeMasters,MergeMastersAdmin)

class MergeStatusAdmin(admin.ModelAdmin):
  pass
admin.site.register(MergeStatus, MergeStatusAdmin)

class MergeRequestAdmin(admin.ModelAdmin):
  list_display = ['branch','status','date']
admin.site.register(MergeRequest, MergeRequestAdmin)

class MergeCommentAdmin(admin.ModelAdmin):
  pass
admin.site.register(MergeComment, MergeCommentAdmin)

class MergeNotificationAdmin(admin.ModelAdmin):
  list_display = ['message','user']
admin.site.register(MergeNotification, MergeNotificationAdmin)

#-*- coding: utf-8 -*-
from django.contrib import admin
from mergemaster.models import *


class MergeMasterAdmin(admin.ModelAdmin):
  list_display = ['user','enabled']
admin.site.register(MergeMaster, MergeMasterAdmin)

class MergeGroupAdmin(admin.ModelAdmin):
    list_display = ['main_branch', 'owner']
admin.site.register(MergeGroup, MergeGroupAdmin)

class MergeRequestAdmin(admin.ModelAdmin):
  list_display = ['branch','date_created']
admin.site.register(MergeRequest, MergeRequestAdmin)

class MergeRequestActionAdmin(admin.ModelAdmin):
    pass
admin.site.register(MergeRequestAction, MergeRequestActionAdmin)

class MergeActionCommentAdmin(admin.ModelAdmin):
  pass
admin.site.register(MergeActionComment, MergeActionCommentAdmin)

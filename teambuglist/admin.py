#-*- coding: utf-8 -*-
from django.contrib import admin
from teambuglist.models import Bug

class BugAdmin(admin.ModelAdmin):
    list_display = ('url','date_add','owner',)
admin.site.register(Bug, BugAdmin)
  
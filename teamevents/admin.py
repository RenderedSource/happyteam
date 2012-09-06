#-*- coding: utf-8 -*-
from django.contrib import admin
from teamevents.models import CalendarEvent

class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title','start','end',)
admin.site.register(CalendarEvent, CalendarEventAdmin)
  
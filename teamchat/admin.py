#-*- coding: utf-8 -*-
from django.contrib import admin
from teamchat.models import UserRoom, Room


__author__ = 'lehabaev'



class UserRoomInline(admin.TabularInline):
    model = UserRoom
    fk_name = "room"

class RoomAdmin(admin.ModelAdmin):
    inlines = [
        UserRoomInline
    ]

admin.site.register(Room, RoomAdmin)
  
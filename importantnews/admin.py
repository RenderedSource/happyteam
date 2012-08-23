#-*- coding: utf-8 -*-
from django.contrib import admin
from importantnews.models import UserRead, News
from django_markdown.admin import MarkdownModelAdmin


__author__ = 'lehabaev'



class UserReadInline(admin.TabularInline):
    model = UserRead
    fk_name = "news"

class NewsAdmin(MarkdownModelAdmin):
    inlines = [
        UserReadInline
    ]
    list_display = ('title','date','author',)

admin.site.register(News, NewsAdmin)
  
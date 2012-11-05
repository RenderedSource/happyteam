#-*- coding: utf-8 -*-
from django.contrib import admin
from teammanagment.models import DeveloperTeam, Team, Sprint, Task, TaskCategory


__author__ = 'lehabaev'



class DeveloperTeamInline(admin.TabularInline):
    model = DeveloperTeam
    fk_name = "team"

class TeamAdmin(admin.ModelAdmin):
    inlines = [
        DeveloperTeamInline
    ]
    list_display = ('title','manager','team_lead',)

admin.site.register(Team, TeamAdmin)

class SprintAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sprint, SprintAdmin)

class TaskCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(TaskCategory, TaskCategoryAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','status','start_date','end_date_actual')
admin.site.register(Task, TaskAdmin)
#-*- coding: utf-8 -*-
from django.contrib import admin
from scrum.models import Team, UserTeam, Project, TeamProject, Sprint, Story, Task


__author__ = 'lehabaev'



class UserTeamAdmin(admin.TabularInline):
    model = UserTeam
    fk_name = "team"

class TeamAdmin(admin.ModelAdmin):
    inlines = [
        UserTeamAdmin
    ]
    list_display = ('leader','name',)
admin.site.register(Team, TeamAdmin)


class TeamProjectAdmin(admin.TabularInline):
    model = TeamProject
    fk_name = "project"

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        TeamProjectAdmin
    ]
admin.site.register(Project, ProjectAdmin)

class SprintAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sprint, SprintAdmin)


class TaskAdmin(admin.TabularInline):
    model = Task
    fk_name = "story"

class StoryAdmin(admin.ModelAdmin):
    inlines = [
        TaskAdmin
    ]
admin.site.register(Story, StoryAdmin)

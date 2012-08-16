import datetime
from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    leader = models.ForeignKey(User)
    name = models.CharField(max_length=60)
    def __unicode__(self):
        return self.name

class UserTeam(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)

class Project(models.Model):
    title = models.CharField(max_length=60)
    status = models.BooleanField(verbose_name='Open?', default=True)
    desc = models.TextField(blank=True)
    owner = models.ForeignKey(User, verbose_name=u'Product owner')

    def __unicode__(self):
        return self.title

class TeamProject(models.Model):
    team = models.ForeignKey(Team)
    project = models.ForeignKey(Project)

class Sprint(models.Model):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=60)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()

    def __unicode__(self):
        return '%s (%s)'%(self.title, self.project.title)

    def getEnd(self):
        delta = datetime.datetime.now() - self.date_finish
        return '%s'%delta

class Story(models.Model):
    sprint = models.ForeignKey(Sprint)
    title = models.CharField(max_length=60)
    deadline = models.DateTimeField()
    requester = models.ForeignKey(User, related_name='requester')
    owner = models.ForeignKey(User, blank=True, related_name='owner')
    desc = models.TextField()
    points = models.IntegerField()
    date_add = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_finish = models.DateTimeField(blank=True, null=True)
    def __unicode__(self):
        return self.title

class Task(models.Model):
    story = models.ForeignKey(Story)
    status = models.BooleanField()
    text = models.CharField(max_length=150)



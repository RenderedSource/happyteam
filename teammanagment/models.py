from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class Team(models.Model):
    title = models.CharField(max_length=60)
    manager = models.ForeignKey(User, related_name='manager')
    team_lead = models.ForeignKey(User, related_name='team_lead')

    def __unicode__(self):
        return self.title

class DeveloperTeam(models.Model):
    team = models.ForeignKey(Team)
    developer = models.ForeignKey(User)

    def __unicode__(self):
        return self.developer.username
    def get_dev_url(self):
        return ''

class Sprint(models.Model):
    number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return 'Sprint %d' %self.number

    def last_finish_tasks(self):
        task = Task.objects.all().order_by('-end_date_actual')[0]
        return task

    def get_tasks_url(self):
        return reverse('sprint_list',args=[self.id])

class TaskCategory(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField()
    icon = models.CharField(max_length=60, blank=True)

    def __unicode__(self):
        return self.title

class Task(models.Model):
    status = models.BooleanField(default=False, help_text=u'Task finish ?')
    title = models.CharField(max_length=60)
    sprint = models.ForeignKey(Sprint)
    desc = models.TextField(blank=True)
    type = models.ForeignKey(TaskCategory)
    developer = models.ForeignKey(DeveloperTeam, null=True)
    start_date = models.DateField()
    end_date_theory = models.DateField(blank=True, null=True)
    end_date_actual = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return 'Sprint %d: %s' %(self.sprint.number, self.title)

    def get_absolute_url(self):
        return reverse('task',args=[self.id])

    def fail_status(self):
        if self.end_date_actual:
            if self.end_date_actual > self.end_date_theory:
                return 'error'
            else:
                return 'success'
        else:
            return 'info'
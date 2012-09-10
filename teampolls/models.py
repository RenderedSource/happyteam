from django.contrib.auth.models import User
from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=60)
    owner = models.ForeignKey(User)
    required = models.BooleanField(help_text=u'If true send email all user')
    multi_select = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class PollVariant(models.Model):
    poll = models.ForeignKey(Poll)
    title = models.CharField(max_length=60)


class UserAnswer(models.Model):
    user = models.ForeignKey(User)
    variant = models.ForeignKey(PollVariant)
    def __unicode__(self):
        return self.user.username

from django.contrib.auth.models import User
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from teamevents.models import CalendarEvent

ROLES = (
    ('developer', 'developer'),
    ('manager', 'manager'),
    ('owner', 'owner'),
    ('client', 'client'),
    )

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = ThumbnailerImageField(upload_to='avatar', blank=True)
    position = models.CharField(max_length=60, choices=ROLES)
    birthday = models.DateField()

    def __unicode__(self):
        return self.user.username


from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
import re

class MacAddress(models.Model):
    user = models.ForeignKey(User)
    address = models.CharField(max_length=17)

    def clean(self):
        mac_re = re.compile(r'^([0-9a-fA-F]{2}([:-]?|$)){6}$')
        if not mac_re.match(self.address):
            raise ValidationError('Invalid MAC address')
        self.address = self.address.upper().replace('-', ':')

    def __unicode__(self):
        return self.address


class GcLoosers(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

class Room(models.Model):
    title = models.CharField(max_length=60)
    css_class = models.CharField(max_length=60, blank=True)
    width = models.IntegerField()
    height = models.IntegerField()
    def __unicode__(self):
        return self.title

class Seat(models.Model):
    SEAT_CSS_CLASS = (
        ('long','long'),
        ('width','width'),
        ('circle','circle')
    )
    room = models.ForeignKey(Room)
    css_class = models.CharField(max_length=60, choices=SEAT_CSS_CLASS)
    user = models.ForeignKey(User, blank=True, null=True)
    x_pos = models.IntegerField()
    y_pos = models.IntegerField()


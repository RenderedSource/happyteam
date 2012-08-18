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

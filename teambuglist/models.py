from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

class Bug(models.Model):
    url = models.CharField(max_length=60)
    status = models.BooleanField(default=False, help_text=u'Bug is fixed?')
    check = models.BooleanField(default=False, help_text=u'Check')
    priority = models.IntegerField(default=0, help_text='0 - 5 high priority')
    desc = models.TextField()
    image = ThumbnailerImageField(upload_to='static/bugs', blank=True)
    owner = models.ForeignKey(User, related_name='bug_owner')
    requester = models.ForeignKey(User, related_name='bug_requester')
    date_add = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url
    def get_absolute_url(self):
        return reverse('bug',args=[self.id])
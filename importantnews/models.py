from django.contrib.auth.models import User
from django.db import models

class News(models.Model):
    author = models.ForeignKey(User)
    required = models.BooleanField(help_text=u'All user required read this news')
    title = models.CharField(max_length=60)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return '/news/%d/'%(self.id)

class UserRead(models.Model):
    news = models.ForeignKey(News)
    user = models.ForeignKey(User)



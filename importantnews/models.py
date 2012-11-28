from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from website.views import SendAllUser

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
    def get_edit_url(self):
        return '/news/edit/%s/'%self.id
    def get_read_user(self):
        return UserRead.objects.filter(news = self)

#    send required new news
    def save(self):
        try:
            News.objects.get(id = self.id)
            super(News, self).save()

        except News.DoesNotExist:
            super(News, self).save()
            message = render_to_string('importantnews/mail.html',{'news':self})
            subject = self.title
            SendAllUser(subject, message)

class UserRead(models.Model):
    news = models.ForeignKey(News)
    user = models.ForeignKey(User)



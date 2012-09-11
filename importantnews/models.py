from audioop import reverse
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from mailer import send_mail, send_html_mail
from website import settings

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
        if self.required:
            try:
                News.objects.get(id = self.id)
            except News.DoesNotExist:
                for user in User.objects.all().values_list('email', flat = True):
                    send_html_mail(self.title,render_to_string('importantnews/mail.html',{'news':self}) ,render_to_string('importantnews/mail.html',{'news':self}), settings.EMAIL_HOST_USER,
                    [user])
        super(News, self).save()

class UserRead(models.Model):
    news = models.ForeignKey(News)
    user = models.ForeignKey(User)



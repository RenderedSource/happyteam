#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template import Context, loader
from django.http import HttpResponse
from mailer import send_html_mail
from website import settings

__author__ = 'lehabaev'
#todo delete this after create normal code
def Index(request):
    return render_to_response('index.html', {}
        , RequestContext(request))

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render(Context()))

def SendAllUser(subject, message):
    """
    send html email for all users
    """
    for user in User.objects.all().values_list('email', flat = True):
        send_html_mail(subject,message ,message, settings.EMAIL_HOST_USER,
        [user])


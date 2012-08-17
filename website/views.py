#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from scrum.models import Sprint

__author__ = 'lehabaev'
#todo delete this after create normal code
def Index(request):
    try:
        sprint = Sprint.objects.all().order_by('-date_start')[0]
    except :
        sprint = False
    return render_to_response('index.html', {'last_sprint': sprint}
        , RequestContext(request))
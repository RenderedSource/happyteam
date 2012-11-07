#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from teammanagment.forms import ItemDailyTaskForm
from teammanagment.models import ItemDailyTask

__author__ = 'lehabaev'
def taskStatus(request):
    if request.POST:
        task = get_object_or_404(ItemDailyTask, id = request.POST.get('task'))

    else:
        return HttpResponse('{"success":"false","message":"Request error"}')
#-*- coding: utf-8 -*-
from django import forms
from teammanagment.models import ItemDailyTask, Task

__author__ = 'lehabaev'
class ItemDailyTaskForm(forms.ModelForm):
    class Meta:
        model = ItemDailyTask

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = [
            'end_date_actual','status'
        ]

class ItemDailyTaskForm(forms.ModelForm):
    class Meta:
        model = ItemDailyTask
        exclude = [
            'day','task','status'
        ]

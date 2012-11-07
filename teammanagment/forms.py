#-*- coding: utf-8 -*-
from django import forms
from teammanagment.models import ItemDailyTask

__author__ = 'lehabaev'
class ItemDailyTaskForm(forms.ModelForm):
    class Meta:
        model = ItemDailyTask

#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from teambuglist.models import Bug

__author__ = 'lehabaev'

class actionForm(forms.Form):
    bug = forms.ModelChoiceField(queryset=Bug.objects.all())
    user = forms.ModelChoiceField(queryset=User.objects.all())

class fixForm(forms.Form):
    bug = forms.ModelChoiceField(queryset=Bug.objects.all())

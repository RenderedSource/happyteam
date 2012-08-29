#-*- coding: utf-8 -*-
from django import forms
from garbagecollector.models import GcLoosers

__author__ = 'lehabaev'
class LooserForm(forms.ModelForm):
    class Meta:
        model = GcLoosers
#-*- coding: utf-8 -*-
from django import forms
from importantnews.models import UserRead, News

__author__ = 'lehabaev'
class ReadNewsForm(forms.ModelForm):
    class Meta:
        model = UserRead
        widgets ={
            'news':forms.HiddenInput(),
            'user':forms.HiddenInput()
        }


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        widgets = {
            'author':forms.HiddenInput(),
        }
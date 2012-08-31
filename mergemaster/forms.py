#-*- coding: utf-8 -*-
from django import forms
from mergemaster.models import MergeRequest, MergeRequestAction

class MergeRequestFormApi(forms.ModelForm):
    class Meta:
        model = MergeRequest
    def __init__(self, *args, **kwargs):
        super(MergeRequestFormApi, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

class MergeRequestForm(forms.ModelForm):
    class Meta:
        model = MergeRequest
        fields = ['branch', 'task_id']

class MergeRequestActionForm(forms.ModelForm):
    class Meta:
        model = MergeRequestAction
        widgets = {
            'merge_request': forms.HiddenInput(),
            'merge_master': forms.HiddenInput(),
            'status': forms.HiddenInput(),
        }
        exclude = ['merge_master', 'reason']

class FilterListForm(forms.Form):
    filters = forms.MultipleChoiceField(
        label = "",
        choices = MergeRequest.STATUS_CHOICES,
        widget = forms.CheckboxSelectMultiple
    )


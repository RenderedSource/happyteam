#-*- coding: utf-8 -*-
from django import forms
from mergemaster.models import MergeRequest, MergeMaster, MergeRequestAction

class MergeRequestFormApi(forms.ModelForm):
    class Meta:
        model = MergeRequest
    def __init__(self, *args, **kwargs):
        super(MergeRequestFormApi, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

#class MergeCommentForm(forms.ModelForm):
#  last_message = forms.IntegerField(required=False, widget=forms.HiddenInput())
#  class Meta:
#    model = MergeComment
#    widgets={
#     'user':forms.HiddenInput(),
#      'merge_request':forms.HiddenInput()
#    }

class MergeRequestForm(forms.ModelForm):
    class Meta:
        model = MergeRequest
        fields = ['developer', 'branch', 'task_id']
        #widgets = {
        #'developer':forms.HiddenInput(),
        #}]

class MergeReqestActionForm(forms.ModelForm):
    class Meta:
        model = MergeRequestAction
        widgets = {
            'merge_request':forms.HiddenInput(),
        }

#class MergeMasterForm(forms.ModelForm):
#  class Meta:
#    model = MergeMaster
#    exclude=['user','enabled',]

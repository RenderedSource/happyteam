#-*- coding: utf-8 -*-
from django import forms
import widgets
from mergemaster.models import MergeRequest,\
    MergeRequestAction, MergeActionComment, REQUEST_STATUS_CHOICES, STATUS_CHOICES

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
        fields = ['branch', 'task_id', 'merge_group']

class MergeRequestActionForm(forms.ModelForm):
    class Meta:
        model = MergeRequestAction
        widgets = {
            'merge_request': forms.HiddenInput(),
            'new_merge_status': widgets.ButtonGroup(choices = REQUEST_STATUS_CHOICES),
            'new_cr_status': widgets.ButtonGroup(choices = STATUS_CHOICES),
            'new_qa_status': widgets.ButtonGroup(choices = STATUS_CHOICES)
        }
        exclude = ['user',]

class MergeActionCommentForm(forms.ModelForm):
    class Meta:
        model = MergeActionComment
        widgets = {
            'merge_action': forms.HiddenInput()
            }
        exclude = ['user',]

class FilterListForm(forms.Form):
    filters = forms.MultipleChoiceField(
        label = "",
        #choices = MergeRequest.STATUS_CHOICES,
        widget = forms.CheckboxSelectMultiple
    )


#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import models
from mergemaster.models import MergeRequest, MergeActionComment

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
        model = MergeRequest
        fields = ['merge_status', 'cr_status', 'qa_status']
        widgets = {
            'merge_request': forms.HiddenInput(),
#            'merge_status': widgets.ButtonGroup(),
#            'cr_status': widgets.ButtonGroup(),
#            'qa_status': widgets.ButtonGroup()
        }
        exclude = ['developer', 'branch']

class MergeActionCommentForm(forms.ModelForm):
    class Meta:
        model = MergeActionComment
        widgets = {
            'merge_action': forms.HiddenInput()
            }
        exclude = ['user',]


class UserModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class FilterListForm(forms.Form):
    user = UserModelChoiceField(
        queryset=User.objects.all(),label = "Filter by developer",
        widget=forms.CheckboxSelectMultiple()
    )
    merge_group = forms.ModelMultipleChoiceField(
        queryset=models.MergeGroup.objects.all(),label = "Filter by merge group",
        widget=forms.CheckboxSelectMultiple()
    )
    include = forms.MultipleChoiceField(
        label = "Filter by status",
        choices = (
            (models.REQUEST_MERGED, 'Show merged requests'),
            (models.REQUEST_SUSPENDED, 'Show suspended resquests'),
        ),
        widget = forms.CheckboxSelectMultiple
    )

class SendFrom(forms.Form):
    user = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),label = "Select subscribe"
    )
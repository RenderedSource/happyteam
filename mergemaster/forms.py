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
        exclude = ['developer', 'branch']

    last_action_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
        expected_last_action_id = int(self.cleaned_data['last_action_id'])
        if expected_last_action_id is not None and self.instance is not None:
            last_action_id = self.instance.get_last_action_id()
            if last_action_id is not None and last_action_id != expected_last_action_id:
                raise forms.ValidationError('Your merge request state is not up-to-date')
        return super(MergeRequestActionForm, self).clean()

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
        queryset=User.objects.all().order_by('first_name'),label = "Filter by developer",
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
    user_send = UserModelChoiceField(
        widget=forms.CheckboxSelectMultiple(),
    queryset=User.objects.all().order_by('first_name'),label = "Select subscribe"
    )
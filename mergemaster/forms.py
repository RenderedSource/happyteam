#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from git.repo.base import Repo
import models
from mergemaster.models import MergeRequest, MergeActionComment
from website.settings import REPO_PATH

class MergeRequestFormApi(forms.ModelForm):
    class Meta:
        model = MergeRequest
    def __init__(self, *args, **kwargs):
        super(MergeRequestFormApi, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

def getBranchList():
    return [(str(x).replace('origin/',''), str(x).replace('origin/','')) for x in Repo(REPO_PATH).remotes.origin.refs]

class MergeRequestForm(forms.ModelForm):

    class Meta:
        model = MergeRequest
        fields = ['branch', 'task_id', 'merge_group']
        widgets = {
            'branch':forms.Select(
                choices=getBranchList()
            )
        }
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
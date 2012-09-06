# coding: utf-8
from django.core.urlresolvers import reverse
import xmpp
import datetime
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import simplejson
from mergemaster.forms import MergeRequestForm, MergeRequestActionForm, MergeActionCommentForm, FilterListForm
from mergemaster.models import MergeRequest, MergeRequestAction, MergeActionComment

def merge_list(request):
    merge_list = MergeRequest.objects.all().order_by('-id')

    return render_to_response(
        'mergemaster/list.html', {
            'merge_list': merge_list,
            'request_form': MergeRequestForm(),
            'action_form': MergeRequestActionForm(),
            'comment_form': MergeActionCommentForm(),
            'filter_form': FilterListForm(),
            'merge_action_list': MergeRequestAction.ACTION_CHOICES
        },
        context_instance=RequestContext(request))

@require_http_methods(["POST"])
def add_merge_request(request):
    request_form = MergeRequestForm(request.POST)
    response_data = {}
    if request_form.is_valid():
        merge_request = request_form.save(commit=False)
        merge_request.developer = request.user
        merge_request.save()

        response_data['success'] = True
        response_data['html'] = render_to_string(
            'mergemaster/merge-table-row.html', {
                'merge': merge_request,
                'action_form': MergeRequestActionForm(),
                'comment_form': MergeActionCommentForm(),
                'merge_action_list': MergeRequestAction.ACTION_CHOICES
            },
            context_instance=RequestContext(request)
        )
    else:
        response_data['success'] = False
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/javascript')

@require_http_methods(["POST"])
def add_merge_action(request):
    action_form = MergeRequestActionForm(request.POST)
    response_data = {}
    if action_form.is_valid():
        action = action_form.save(commit=False)
        action.user = request.user
        action.save()

        action_form = MergeRequestActionForm()

        response_data['success'] = True
        response_data['merge_id'] = action.merge_request.id
        response_data['actions_html'] = render_to_string(
            'mergemaster/merge-table-row-actions.html', {
                'merge': action.merge_request,
                'action_form': action_form,
                'comment_form': MergeActionCommentForm(),
                'merge_action_list': MergeRequestAction.ACTION_CHOICES
            },
            context_instance=RequestContext(request)
        )
        response_data['head_html'] = render_to_string(
            'mergemaster/merge-table-row-head.html', {
                'merge': action.merge_request
            },
            context_instance=RequestContext(request)
        )
        response_data['buttons_html'] = render_to_string(
            'mergemaster/merge-table-row-buttons.html', {
                'merge': action.merge_request,
                'action_form': action_form,
            },
            context_instance=RequestContext(request)
        )
    else:
        response_data['success'] = False
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/javascript')

@require_http_methods(["POST"])
def add_action_comment(request):
    comment_form = MergeActionCommentForm(request.POST)
    response_data = {}
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.save()

        response_data['success'] = True
        response_data['action_id'] = comment.merge_action.id
        response_data['comments_html'] = render_to_string(
            'mergemaster/action-comments.html', {
                'action': comment.merge_action,
                'comment_form': MergeActionCommentForm(),
                'merge_action_list': MergeRequestAction.ACTION_CHOICES
            },
            context_instance=RequestContext(request)
        )
        response_data['comment_count_html'] = render_to_string(
            'mergemaster/action-comment-count.html', {
                'action': comment.merge_action
            },
            context_instance=RequestContext(request)
        )
    else:
        response_data['success'] = False
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/javascript')

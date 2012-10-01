# coding: utf-8
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import render_to_string
import simplejson
from mergemaster.forms import MergeRequestForm, MergeRequestActionForm, MergeActionCommentForm, FilterListForm
from mergemaster.models import MergeRequest, MergeRequestAction
from django.db import transaction
from django.db.models import Count

def merge_list(request):
    merge_list = MergeRequest.objects.all()\
        .prefetch_related('merge_group').prefetch_related('developer')\
        .annotate(Count('mergerequestaction'))\
        .order_by('-id')

    return render_to_response(
        'mergemaster/list.html', {
            'merge_list': merge_list,
            'request_form': MergeRequestForm(),
            'filter_form': FilterListForm()
        },
        context_instance=RequestContext(request))

def merge_details(request, merge_id):
    merge_request = MergeRequest.objects\
        .select_related(
            'mergerequestaction__mergeactioncomment',
            'mergerequestaction__mergeactioncomment__user',
            'mergerequestaction__user'
        ).get(id = merge_id)
    return render_to_response(
        'mergemaster/request-subrow.html', {
            'merge': merge_request,
            'action_form': MergeRequestActionForm(initial={
                'merge_status': merge_request.merge_status,
                'cr_status': merge_request.cr_status,
                'qa_status': merge_request.qa_status
            }),
            'comment_form': MergeActionCommentForm(),
            'filter_form': FilterListForm()
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

        # reload to update related objects
        merge_request = MergeRequest.objects.all()\
            .select_related('merge_group').select_related('developer')\
            .annotate(Count('mergerequestaction'))\
            .get(id = merge_request.id)

        response_data['success'] = True
        response_data['html'] = render_to_string(
            'mergemaster/request-row.html', {
                'merge': merge_request,
                'action_form': MergeRequestActionForm(),
                'comment_form': MergeActionCommentForm()
            },
            context_instance=RequestContext(request)
        )
    else:
        response_data['success'] = False
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/javascript')

@require_http_methods(["POST"])
@transaction.commit_on_success
def update_merge_request(request, merge_id):
    try:
        merge_request = MergeRequest.objects.get(id = merge_id)
    except MergeRequest.DoesNotExist:
        raise Http404

    old_merge_status = merge_request.merge_status
    old_cr_status = merge_request.cr_status
    old_qa_status = merge_request.qa_status

    action_form = MergeRequestActionForm(request.POST, instance=merge_request)
    response_data = {}
    if action_form.is_valid():
        action_form.save()

        request_changed = False
        action = MergeRequestAction()
        if merge_request.merge_status != old_merge_status:
            action.new_merge_status = merge_request.merge_status
            request_changed = True
        if merge_request.cr_status != old_cr_status:
            action.new_cr_status = merge_request.cr_status
            request_changed = True
        if merge_request.qa_status != old_qa_status:
            action.new_qa_status = merge_request.qa_status
            request_changed = True

        if request_changed:
            action.merge_request = merge_request
            action.user = request.user
            action.save()

        # reload to update related objects
        merge_request = MergeRequest.objects.all()\
            .select_related('merge_group').select_related('developer')\
            .annotate(Count('mergerequestaction'))\
            .get(id = merge_id)

        response_data['success'] = True
        response_data['merge_id'] = merge_request.id
        response_data['actions_html'] = render_to_string(
            'mergemaster/request-actions.html', {
                'merge': merge_request,
                'action_form': MergeRequestActionForm(),
                'comment_form': MergeActionCommentForm(),
            },
            context_instance=RequestContext(request)
        )
        response_data['head_html'] = render_to_string(
            'mergemaster/request-head.html', {
                'merge': merge_request
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
                'comment_form': MergeActionCommentForm()
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

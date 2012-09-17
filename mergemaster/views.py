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

def merge_list(request):
    merge_list = MergeRequest.objects.all().order_by('-id')

    return render_to_response(
        'mergemaster/list.html', {
            'merge_list': merge_list,
            'request_form': MergeRequestForm(),
            'action_form': MergeRequestActionForm(),
            'comment_form': MergeActionCommentForm(),
            'filter_form': FilterListForm()
        },
        context_instance=RequestContext(request))

def merge_details(request, merge_id):
    merge_request = MergeRequest.objects.get(id = merge_id)
    return render_to_response(
        'mergemaster/request-subrow.html', {
            'merge': merge_request,
            'request_form': MergeRequestForm(),
            'action_form': MergeRequestActionForm(),
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

    print merge_id

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

        action = MergeRequestAction()
        action.merge_request = merge_request
        action.new_merge_status = merge_request.merge_status if merge_request.merge_status != old_merge_status else None
        action.new_cr_status = merge_request.cr_status if merge_request.cr_status != old_cr_status else None
        action.new_qa_status = merge_request.qa_status if merge_request.qa_status != old_qa_status else None
        action.user = request.user
        action.save()

        action_form = MergeRequestActionForm()

        response_data['success'] = True
        response_data['merge_id'] = action.merge_request.id
        response_data['actions_html'] = render_to_string(
            'mergemaster/request-actions.html', {
                'merge': action.merge_request,
                'action_form': action_form,
                'comment_form': MergeActionCommentForm(),
                #'merge_action_list': MergeRequestAction.ACTION_CHOICES
            },
            context_instance=RequestContext(request)
        )
        response_data['head_html'] = render_to_string(
            'mergemaster/request-head.html', {
                'merge': action.merge_request
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

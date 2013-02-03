# coding: utf-8
from django.core.serializers import json
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.template.loader import render_to_string
import simplejson
from mailer import send_html_mail
from mergemaster.forms import MergeRequestForm, MergeRequestActionForm, MergeActionCommentForm, FilterListForm, SendFrom
from mergemaster.models import MergeRequest, MergeRequestAction
from django.db import transaction
from django.db.models import Count
import models
from website import settings
from website.settings import REPO_PATH
from git import *
from diff import Visualizer

def merge_list(request, selected_merge_id):
    template_data = {}
    selected_merge_id = int(selected_merge_id) if selected_merge_id is not None else None
    if selected_merge_id is not None:
        try:
            merge_request = MergeRequest.objects.get(id = selected_merge_id)
            template_data['action_form'] = MergeRequestActionForm(initial={
                'merge_status': merge_request.merge_status,
                'cr_status': merge_request.cr_status,
                'qa_status': merge_request.qa_status
            })
            user_list = MergeRequestAction.objects.filter(merge_request = merge_request)\
            .exclude(user = request.user).distinct()
            user_list = user_list.values_list('user__id', flat=True)
            template_data['send_form'] = SendFrom(initial={'user_send':user_list})
        except MergeRequest.DoesNotExist:
            return redirect('mergemaster.views.merge_list')

    include = [int(i) for i in request.GET.getlist('include', [])]
    merge_list = MergeRequest.objects.all()\
        .prefetch_related('merge_group').prefetch_related('developer')\
        .annotate(Count('mergerequestaction'))\
        .order_by('-id')
    if request.GET.getlist('user',[]):
        merge_list = merge_list.filter(developer__in = request.GET.getlist('user',[]))
    if request.GET.getlist('merge_group',[]):
        merge_list = merge_list.filter(merge_group__in = request.GET.getlist('merge_group',[]))
    if models.REQUEST_MERGED not in include:
        merge_list = merge_list.exclude(merge_status=models.REQUEST_MERGED)
    if models.REQUEST_SUSPENDED not in include:
        merge_list = merge_list.exclude(merge_status=models.REQUEST_SUSPENDED)

    template_data['merge_list'] = merge_list
    template_data['selected_merge_id'] = selected_merge_id

    if request.is_ajax():
        return render_to_response(
            'mergemaster/list.html',
            template_data,
            context_instance=RequestContext(request))
    else:
        template_data.update({
            'request_form': MergeRequestForm(),
            'filter_form': FilterListForm()
        })
        return render_to_response(
            'mergemaster/index.html',
            template_data,
            context_instance=RequestContext(request))

def merge_details(request, merge_id):
    merge_request = MergeRequest.objects\
        .select_related(
            'mergerequestaction__mergeactioncomment',
            'mergerequestaction__mergeactioncomment__user',
            'mergerequestaction__user'
        ).get(id = merge_id)
    user_list = MergeRequestAction.objects.filter(merge_request = merge_request).exclude(user = request.user).distinct()
    user_list = user_list.values_list('user__id', flat=True)
    return render_to_response(
        'mergemaster/request-subrow.html', {
            'merge': merge_request,
            'send_form':SendFrom(initial={'user_send':user_list}),
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
#    todo send message team lead
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
        # todo in progress change user to owner
        if request.POST.getlist('user_send',[]):
            send_form = SendFrom(request.POST)
            if send_form.is_valid():
                for user in send_form.cleaned_data['user_send']:
                    message = render_to_string('mergemaster/email/message-need-merge.txt',{'merge':merge_request})
                    subject = 'Need merge branch #%d' % merge_request.id
                    send_html_mail('[RS] ' + subject,message ,message, settings.EMAIL_HOST_USER,
                        [user.email])
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
        #    send notification
        if request.POST.getlist('user_send',[]):
            send_form = SendFrom(request.POST)
            if send_form.is_valid():
                for user in send_form.cleaned_data['user_send']:
                    if merge_request.merge_status == 2:
                        message = render_to_string('mergemaster/email/message-merged.txt',
                                {
                                'branch':merge_request.branch,
                                'merge_group':merge_request.merge_group,
                                'user':request.user.get_full_name
                            })
                    elif merge_request.cr_status == 2 or merge_request.qa_status == 2:
                        message = render_to_string('mergemaster/email/message-reject.txt',
                                {
                                'branch':merge_request.branch,
                                'merge_group':merge_request.merge_group,
                                'url':merge_request.id,
                                'user':request.user.get_full_name
                            })
                    else:
                        message = render_to_string('mergemaster/email/message.txt',
                                {
                                'merge':merge_request,
                                'branch':merge_request.branch,
                                'user':request.user.get_full_name
                            })

                    subject = 'Change status request #%d' % merge_request.id

                    send_html_mail('[RS] ' + subject,message ,message, settings.EMAIL_HOST_USER,
                        [user.email])
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

def diff(request, from_branch, to_branch):
    try:
        repo = Repo(REPO_PATH)
    except NoSuchPathError:
        return HttpResponseNotFound('Git repository not found. Check REPO_PATH')

    origin = repo.remotes.origin
    if from_branch not in origin.refs:
        return HttpResponseNotFound('Branch %s not found' % from_branch)
    origin = repo.remotes.origin
    if to_branch not in origin.refs:
        return HttpResponseNotFound('Branch %s not found' % to_branch)

    patch = repo.git.diff('origin/%s...origin/%s' % (to_branch, from_branch), find_renames=True)
    visualizer = Visualizer()
    diffs = visualizer.parse(patch)

    return render_to_response(
        'mergemaster/diff.html', {
            'from_branch': from_branch,
            'to_branch': to_branch,
            'diffs': diffs
        },
        context_instance=RequestContext(request))

def getBranchList(request):
    repo = Repo(REPO_PATH)
#    repo.remotes.origin.fetch()
    list = []
    for x in repo.remotes.origin.refs:
        list.append((str(x).replace('origin/','')))
    return HttpResponse(json.simplejson.dumps(list))
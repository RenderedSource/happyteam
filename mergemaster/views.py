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
from mergemaster.forms import MergeRequestForm, MergeRequestFormApi, MergeReqestActionForm
from mergemaster.models import MergeRequest, MergeMaster, MergeNotification, JabberMessage, MergeRequestAction
from website import settings

def merge_list(request):
    merge_list = MergeRequest.objects.all().order_by('-id')

    merge_request_form = MergeRequestForm()
    merge_action_form = MergeReqestActionForm()

    return render_to_response('mergemaster/list.html',
        {
            'merge_list': merge_list,
            'request_form': merge_request_form,
            'action_form': merge_action_form,
            'merge_action_list': MergeRequestAction.ACTIONS
        },
        context_instance=RequestContext(request))

@require_http_methods(["POST"])
def add_merge_request(request):
    request_form = MergeRequestForm(request.POST)
    valid = False
    if request_form.is_valid():
        merge_request = request_form.save(commit=False)
        merge_request.developer = request.user
        merge_request.save()
        valid = True
    return HttpResponse(simplejson.dumps({ 'success': valid }), mimetype='application/javascript')

@require_http_methods(["POST"])
def add_merge_action(request):
    action_form = MergeReqestActionForm(request.POST)
    valid = False
    if action_form.is_valid():
        action = action_form.save(commit=False)
        action.merge_master = MergeMaster.objects.get(user=request.user, enabled=True)
        action.save()
        valid = True
    return HttpResponse(simplejson.dumps({ 'success': valid }), mimetype='application/javascript')


def SendJabber(request):
    try:
        jid = xmpp.protocol.JID(settings.JABBER_ID)
        cl = xmpp.Client(jid.getDomain(), debug=[])
        conn = cl.connect()
        sended_messages = 0
        if conn:
            auth = cl.auth(jid.getNode(), settings.JABBER_PASSWORD,
                resource=jid.getResource())
            if auth:
                for item in JabberMessage.objects.filter(date__gte=datetime.datetime.now() - datetime.timedelta(1)):
                    cl.send(xmpp.protocol.Message(item.jabber, item.text))
                    item.delete()
                    sended_messages = sended_messages + 1
        return HttpResponse('%s' % sended_messages)

    except JabberMessage.DoesNotExist:
        return HttpResponse('All sended')


def JabberNotificate(message, recipient):
    JabberMessage.objects.create(jabber=recipient, text=message).save()


@csrf_exempt
def ApiAddRequest(request):
    """
    API add new request, git hook send new request and user email
    curl -X POST -d 'email=rizmailov@renderedsource.com&branch=new_branch2&status=1' 127.0.0.1:8000/merge/api/ > page.html
    """
    #  todo add api key
    form = MergeRequestFormApi(request.POST)

    if form.is_valid():
        form = form.save(commit=False)
        form.developer = User.objects.get(email=request.POST.get('email'))
        form.save()
        message = {
            'text': 'Please merge new branch %s Developer: %s' % (form.branch, form.developer),
            'type': 'info'
        }
        for user in MergeMaster.objects.filter(enabled = True):
            JabberNotificate(message.get('text'), user.user.email)
        for user in User.objects.all():
            MergeNotification.objects.create(message=message.get('text'), type=message.get('type'), user=user,
                request=form.id).save()

    else:
        message = 'Error %s' % form.errors
    return HttpResponse('%s' % message)




def MergeAction(request, action, pid):
    message = ''
    try:
    #    only merge_master
        merge_master = MergeMaster.objects.get(user = request.user, enabled = True)
        if action == 'review' or action == 'approve' or action == 'reject' or action == 'open':
            try:
                mod_merge = MergeRequest.objects.get(Q(merge_master__user=request.user) | Q(merge_master=None), id=pid)
                mod_merge.status = action
                mod_merge.merge_master = merge_master
                if  action == 'open':
                    mod_merge.merge_master = None
                mod_merge.save()
                message = {'text': 'Merge master %s %s %s branch %s' % (
                    merge_master.user.first_name,
                    merge_master.user.last_name,
                    action,
                    mod_merge.branch
                    ), 'type': 'success'}

                #        message to user
                if action == 'reject':
                #            add merge master stat reject because after save redirect to discuss page
                    MergeStats.objects.create(merge_master=merge_master, action=action).save()
                    message = 'Your branch reject please got to chat http://%s%s' % (
                    request.META['HTTP_HOST'], reverse('discuss', args=[mod_merge.id]))
                    JabberNotificate(message, mod_merge.developer.email)
                    return HttpResponseRedirect(reverse('discuss', args=[mod_merge.id]))

                if action == 'review':
                    message_jabber = 'Your branch %s start review %s' % (mod_merge.branch, mod_merge.merge_master)
                if action == 'approve':
                    message_jabber = 'Your branch %s approved and merged' % (mod_merge.branch)
                if message:
                    JabberNotificate(message_jabber, mod_merge.developer.email)


            except MergeRequest.DoesNotExist:
                message = {'text': 'No find request or another merge master', 'type': 'error'}

        if action == 'delete':
            try:
                del_r = MergeRequest.objects.get(Q(merge_master=request.user) | Q(merge_master=None), id=pid)
                del_r.delete()
                message = {'text': 'Merge master %s %s delete branch %s' % (
                    merge_master.user.first_name,
                    merge_master.user.last_name,
                    del_r.branch
                    ), 'type': 'success'}
            except MergeRequest.DoesNotExist:
                message = {'text': 'No find request or another merge master', 'type': 'error'}
                #  add merge stat
        #MergeStats.objects.create(merge_master=merge_master, action=action).save()
    except MergeMaster.DoesNotExist:
    #  if your owner
        if action == 'delete':
            try:
                MergeRequest.objects.get(id=pid, developer=request.user).delete()
            except MergeRequest.DoesNotExist:
                message = {'text': 'No find request', 'type': 'error'}
    for user in User.objects.all():
        MergeNotification.objects.create(message=message.get('text'), type=message.get('type'), user=user,
            request=pid).save()

    return HttpResponseRedirect('/merge/')

#При reject создается страница с комментами и при следующих пушах либо делает
# уже без создания нового объекта либо как то продолжается тот.. Дописывается в него и т.д...
@csrf_exempt
def MergeDiscusLoad(request, pid):
    try:
        if request.is_ajax():
            comments_list = MergeComment.objects.filter(merge_request__id=pid, id__gt=request.POST.get('last_message'))
            return render_to_response('mergemaster/discus-message.html', {'comments_list': comments_list})
        else:
            return HttpResponseRedirect('/merge/discus/%s/' % pid)
    except MergeRequest.DoesNotExist:
        raise Http404


def MergeDiscus(request, pid):
    try:
        merge_request = MergeRequest.objects.get(id=pid)
        if request.method == 'POST':
            form = MergeCommentForm(request.POST)
            if form.is_valid():
                form.save()
                if request.is_ajax():
                    comments_list = MergeComment.objects.filter(merge_request__id=pid,
                        id__gt=form.cleaned_data.get('last_message'))
                    return render_to_response('mergemaster/discus-message.html', {'comments_list': comments_list})
                else:
                    return HttpResponseRedirect('/merge/discus/%s/' % pid)
        else:
            form = MergeCommentForm(initial={'user': request.user, 'merge_request': merge_request})

        comments_list = MergeComment.objects.filter(merge_request__id=pid).order_by('-date')

        return render_to_response('mergemaster/discus.html',
                {'merge_request': merge_request, 'comments_list': comments_list, 'form': form},
            context_instance=RequestContext(request))
    except MergeRequest.DoesNotExist or MergeComment.DoesNotExist:
        raise Http404


@csrf_exempt
def AjaxMergeNotification(request):
    try:
        notification_list = MergeNotification.objects.filter(user=request.user).order_by('-date')
        del_id = []
        for item in notification_list: del_id.append(item.id)
        notification_list.filter(id__in=notification_list).delete()
    except MergeNotification.DoesNotExist:
        notification_list = False
    return render_to_response('mergemaster/notification_list.html', {'notification_list': notification_list},
        context_instance=RequestContext(request))


@csrf_exempt
def MergeTableRow(request, pid):
#  if request.is_ajax:
    try:
        merge_request = MergeRequest.objects.get(id=pid)
    except MergeRequest.DoesNotExist:
        merge_request = False
    try:
        merge_master = MergeMasters.objects.get(user=request.user)
    except MergeMasters.DoesNotExist:
        merge_master = False
    actions_html = render_to_string('mergemaster/merge-table-row-actions.html',
            {'merge': merge_request, 'user': request.user, 'merge_master': merge_master})
    jsonDict = {'id': merge_request.id, 'developer': merge_request.developer.username, 'date': '%s' % merge_request.date
        ,
                'actions': actions_html,
                'branch': merge_request.branch, 'merge_master': '%s' % merge_request.merge_master,
                'status': merge_request.status
    }
    return HttpResponse(simplejson.dumps(jsonDict), mimetype="application/json")


def MergeMasterStats(request, pid):
    try:
        merge_master = MergeMasters.objects.get(id=pid)
        merge_stat = MergeStats.objects.filter(merge_master=merge_master)
        reject = merge_stat.filter(action='reject').count()
        cancel = merge_stat.filter(action='cancel').count()
        approve = merge_stat.filter(action='approve').count()
        review = merge_stat.filter(action='review').count()
        delete = merge_stat.filter(action='delete').count()
        return render_to_response('mergemaster/merge_stat.html',
                {'merge_master': merge_master, 'reject': reject, 'cancel': cancel, 'approve': approve, 'reject': reject,
                 'review': review, 'delete': delete},
            context_instance=RequestContext(request))
    except MergeMasters.DoesNotExist:
        raise Http404


def MergeMastersCabinet(request):
    try:
        master = MergeMasters.objects.get(user=request.user)
        if request.method == 'POST':
            form = MergeMastersForm(request.POST, instance=master)
            if form.is_valid():
                form.save()
        form = MergeMastersForm(instance=master)
        return render_to_response('mergemaster/cabinet.html', {'form': form}, RequestContext(request))
    except MergeMasters.DoesNotExist:
        return HttpResponse('You are not merge master')

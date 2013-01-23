# Create your views here.
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
from mailer import send_mail
from teambuglist.forms import actionForm, fixForm
from teambuglist.models import Bug
from website import settings

def bug_list(request):
    bug_list = Bug.objects.all().order_by('-date_add')
    if 'owner' in request.GET:
        bug_list = bug_list.filter(owner = request.GET['owner'])
    if 'requester' in request.GET:
        bug_list = bug_list.filter(requester = request.GET['requester'])
    try:
        if request.GET['status']:
            bug_list = bug_list.filter(status = True)
        else:
            bug_list = bug_list.filter(status = False)
    except :
        bug_list = bug_list.filter(status = False)

    try:
        temp = request.GET['window']
        template = 'buglist/table-content.html'
    except:
        template = 'buglist/buglist.html'
    return render_to_response(template, {'bug_list': bug_list, 'user_list':User.objects.all().order_by('first_name')},
        context_instance=RequestContext(request))

def bug(request, pid):
    return render_to_response('buglist/bug.html', {'bug': get_object_or_404(Bug, id = pid)},
        context_instance=RequestContext(request))

def bug_action(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'change-owner':
            form = actionForm(request.POST)
            if form.is_valid():
                bug = form.cleaned_data['bug']
                user = form.cleaned_data['user']
                bug.owner = user
                bug.save()
                return HttpResponse('success')
            else:
                return HttpResponse('%s'%form.errors)
        if request.POST.get('action') == 'fixForm':
            form = fixForm(request.POST)
            if form.is_valid():
                bug = form.cleaned_data['bug']
                bug.check = True
#                send email to requester
                send_mail(
                    '[RS]Please check bug','Please check this bug because you are owner. <br/><a href="%s">Bug link</a>'
                                           %(str(reverse('bug',args=[bug.id]))),
                    settings.EMAIL_HOST_USER,
                    [bug.requester.email]
                )
                bug.save()
                return HttpResponse('success')
            else:
                return HttpResponse('%s'%form.errors)
        if request.POST.get('action') == 'approve':
            form = fixForm(request.POST)
            if form.is_valid():
                bug = form.cleaned_data['bug']
                bug.status = True
                bug.save()
                return HttpResponse('success')
            else:
                return HttpResponse('%s'%form.errors)

    else:
        return HttpResponse('Not valid')

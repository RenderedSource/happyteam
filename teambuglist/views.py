# Create your views here.
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
from teambuglist.models import Bug

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
        window = request.GET['window']
        template = 'buglist/table-content.html'
    except:
        template = 'buglist/buglist.html'
    return render_to_response(template, {'bug_list': bug_list},
        context_instance=RequestContext(request))

def bug(request, pid):
    return render_to_response('buglist/bug.html', {'bug': get_object_or_404(Bug, id = pid)},
        context_instance=RequestContext(request))
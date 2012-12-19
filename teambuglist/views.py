# Create your views here.
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
from teambuglist.models import Bug

def bug_list(request):
    return render_to_response('buglist/buglist.html', {'bug_list': get_list_or_404(Bug)},
        context_instance=RequestContext(request))

def bug(request, pid):
    return render_to_response('buglist/bug.html', {'bug': get_object_or_404(Bug, id = pid)},
        context_instance=RequestContext(request))
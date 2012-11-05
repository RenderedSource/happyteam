#todo create decorator access deny
from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.template.context import RequestContext
from teammanagment.models import Sprint, Task

def sprint_list(request):
    sprint_list = get_list_or_404(Sprint)
    return render_to_response('sprints-list.html',{'sprint_list':sprint_list},RequestContext(request))

def sprint_tasks(request, pid):
    tasks_list = get_list_or_404(Task, sprint = pid)
    sprint = get_object_or_404(Sprint, id = pid)
    return render_to_response('sprint-tasks.html',{'tasks_list':tasks_list,'sprint':sprint},RequestContext(request))

def task(request, pid):
    task = get_object_or_404(Task, id = pid)
    return render_to_response('task.html',{'task':task},RequestContext(request))

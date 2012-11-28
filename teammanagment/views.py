#todo create decorator access deny
import datetime
from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.template.context import RequestContext
from teammanagment.forms import TaskForm, ItemDailyTaskForm
from teammanagment.models import Sprint, Task, DailyTask

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

def dayTask(request):
#    todo 404
    task_list = DailyTask.objects.filter(user = request.user, day__in = [datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1) ])
    return render_to_response('dayTask.html',{'task_list':task_list},RequestContext(request))

def taskPrice(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
    else:
        task_form = TaskForm()

    return render_to_response('taskPrice.html',{'task_form':task_form},RequestContext(request))

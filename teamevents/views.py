import datetime
import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from teamevents.models import CalendarEvent

def calendar(request):
    return render_to_response('teamevents/calendar.html',{},RequestContext(request))

@csrf_exempt
def calendar_data(request):
    if 'start' in request.POST and 'end' in request.POST:
        start =datetime.datetime.fromtimestamp(float(request.POST.get('start')))
        end =datetime.datetime.fromtimestamp(float(request.POST.get('end')))
        event_list = CalendarEvent.objects.filter(start__gte = start, end__lte = end)
        data = [
            {
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat(),
            'allDay':event.allDay,
            'url':event.url,
            'className':event.class_name,
            'editable':event.editable,
            'color':event.color,
            'backgroundColor':event.background_color,
            'borderColor':event.border_color,
            'textColor':event.text_color,

        } for event in event_list]
    else:
        data = {'success':False}
    return HttpResponse(json.dumps(data), mimetype='application/json')



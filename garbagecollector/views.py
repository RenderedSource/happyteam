import datetime
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from garbagecollector.forms import LooserForm
from garbagecollector.models import Seat, GcLoosers
import network
from website.views import SendAllUser

def index(request):
    return render_to_response('garbagecollector/index.html',{},
        context_instance = RequestContext(request))

def get_online(request):
    mac_addresses = network.get_online_mac_addesses()
    try:
        last_win = GcLoosers.objects.all().order_by('-date')[0].id
        online_users = User.objects.filter(macaddress__address__in = mac_addresses).exclude(
            id = last_win
        ).distinct()
    except :
        online_users = User.objects.filter(macaddress__address__in = mac_addresses).distinct()
    online_ids = online_users.values_list('id', flat=True)
    try:
        offline_users = User.objects.exclude(id__in = online_ids).exclude(
            id = GcLoosers.objects.all().order_by('-date')[0].id
        ).distinct()
    except :
        offline_users = User.objects.exclude(id__in = online_ids).distinct()
    data = map(lambda x: {'id': x.id, 'first_name': x.first_name, 'last_name': x.last_name, 'online': True}, online_users)
    data = data + map(lambda x: {'id': x.id, 'first_name': x.first_name, 'last_name': x.last_name, 'online': False}, offline_users)

    return HttpResponse(json.dumps(data), mimetype='application/json')

def add_looser(request):
    if request.method == 'POST':
        form = LooserForm(request.POST)
        if form.is_valid():
            temp = form.save()
            user_id = temp.user.id
            subject = 'Garbage Collector'
            message = render_to_string('garbagecollector/mail.html',{'date':datetime.datetime.now(), 'user':User.objects.get(id = user_id)})
            SendAllUser(subject, message)
            data={'status' : 1}

        else:
            data={
            'status' : 0,
            'error' : form.errors
            }
    else:
        data = {'status':1, 'error':'No POST'}
    return HttpResponse(data,'application/javascript')
#Todo move to another module
@csrf_exempt
def save_seat(request):
    if request.method == 'POST':
        for seat in request.POST.getlist('seat[]'):
            seat_array = seat.split('|')
            temp = Seat.objects.get(id = seat_array[0])
            temp.x_pos = seat_array[1][:-2]
            temp.y_pos = seat_array[2][:-2]
            temp.save()
        return HttpResponse('All items save')
    else:
        return HttpResponse('No post')
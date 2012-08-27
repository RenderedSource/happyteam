#-*- coding: utf-8 -*-
from django.utils.html import strip_tags
from django_socketio import events
from teamchat.models import UserRoom

__author__ = 'lehabaev'
@events.on_message(channel="team-chat")
def message(request, socket, context, message):
    if message["action"] == "start":
#        name = strip_tags(message["user_id"])
        if message["room"] == '':
            try:
                user = UserRoom.objects.get(user = request.user, session = socket.session.session_id)
            except UserRoom.DoesNotExist:
                user, created = UserRoom.objects.get_or_create(user = request.user)
                user.session = socket.session.session_id
                user.save()
                joined = {"action": "join", "name": user.user.username, "id": user.id}
                socket.send_and_broadcast_channel(joined)
            context["user"] = user
            users = [{'name':u.user.username, 'id':u.id} for u in UserRoom.objects.all().exclude(id = user.id)]
            socket.send({"action": "started", "users": users})

@events.on_finish(channel="team-chat")
def finish(request, socket, context):
    try:
        user = context["user"]
    except KeyError:
        return
    left = {"action": "leave", "name": user.user.username, "id": user.id}
    socket.broadcast_channel(left)
    try:
        UserRoom.objects.get(id = context['user'].id).delete()
    except UserRoom.DoesNotExist:
        return
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def TeamChat(request):
    return render_to_response(
        'teamchat/chat.html',
        {},
        context_instance=RequestContext(request)
    )
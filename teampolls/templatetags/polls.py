from django.shortcuts import get_list_or_404, render_to_response
from teampolls.models import Poll
from django import template

register = template.Library()



@register.inclusion_tag('tags/poll_list.html')
def PollList():
    poll_list = get_list_or_404(Poll)
    return {'poll_list':poll_list}
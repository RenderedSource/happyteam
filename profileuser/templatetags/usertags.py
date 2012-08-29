from django import template
from django.contrib.auth.models import User

register = template.Library()

"""
{% load usertags %}
{% online_users 5 %}
{% last_registers 5 %}
{% last_logins 5 %}

"""

@register.inclusion_tag('tags/online_users.html', takes_context=True)
def online_users(context):
    return {
        'user':context['user']
        }

@register.inclusion_tag('tags/last_logins.html')
def last_logins(num):
    """
    Show last logins ...
    """
    users = User.objects.filter(is_active__exact=1).order_by('-last_login')[:num]
    return {
        'users': users,
        }
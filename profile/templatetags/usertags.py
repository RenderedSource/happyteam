from django import template
from django.contrib.auth.models import User
import datetime

register = template.Library()

"""
{% load usertags %}
{% online_users 5 %}
{% last_registers 5 %}
{% last_logins 5 %}

"""

@register.inclusion_tag('tags/online_users.html')
def online_users(num):
    """
    Show user that has been login an hour ago.
    """
    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    sql_datetime = datetime.datetime.strftime(one_hour_ago, '%Y-%m-%d %H:%M:%S')
    users = User.objects.filter(last_login__gt=sql_datetime,
        is_active__exact=1).order_by('-last_login')[:num]
    return {
        'users': users,
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
from django import template
from django.contrib.auth.models import User
import datetime
from importantnews.models import News

register = template.Library()
__author__ = 'lehabaev'

@register.inclusion_tag('tags/latest_news.html')
def latest_news(num):
    return {'news_list': News.objects.all().order_by('-required', '-date')[:num]}
from django import template
from django.contrib.auth.models import User
import datetime
from django.contrib.comments.models import Comment
from importantnews.models import News

register = template.Library()
__author__ = 'lehabaev'

@register.inclusion_tag('tags/latest_news.html')
def latest_news(num):
    return {'news_list': News.objects.all().order_by('-required', '-date')[:num]}

@register.inclusion_tag('tags/last_comments.html')
def last_comments(num):
    comment_list = Comment.objects.all().order_by('-submit_date')[:num]

    return {"comment_list":comment_list}
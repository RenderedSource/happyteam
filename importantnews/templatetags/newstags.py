from django import template
from django.contrib.auth.models import User
import datetime
from django.contrib.comments.models import Comment
from importantnews.models import News, UserRead
register = template.Library()
__author__ = 'lehabaev'

@register.inclusion_tag('tags/latest_news.html')
def latest_news(num):
    return {'news_list': News.objects.all().order_by('-date')[:num]}

@register.inclusion_tag('tags/last_comments.html')
def last_comments(num):
    comment_list = Comment.objects.all().order_by('-submit_date')[:num]

    return {"comment_list":comment_list}


@register.inclusion_tag('tags/unread_news.html')
def unread_news(user_id):
    read_news = UserRead.objects.filter(user__id=user_id).values_list('news__id', flat=True)
    news_count = News.objects.all().exclude(id__in=read_news).order_by('-date').count()
    return {"news_count":news_count}
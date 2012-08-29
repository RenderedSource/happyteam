#-*- coding: utf-8 -*-
from garbagecollector.models import GcLoosers
from django import template

register = template.Library()

@register.inclusion_tag('tags/gc_last_looser.html')
def last_loosers():
    latest_looser_list = GcLoosers.objects.all().order_by('-date')
    return {
        'latest_looser_list':latest_looser_list
    }
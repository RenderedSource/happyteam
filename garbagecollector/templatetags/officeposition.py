#-*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import User
from garbagecollector import network
from garbagecollector.models import Seat


register = template.Library()

@register.inclusion_tag('tags/team_position.html')
def who_in_office():
    try:
        mac_addresses = network.get_online_mac_addesses()
        online_users = User.objects.filter(macaddress__address__in = mac_addresses).distinct()
    except :
        online_users = False
    seat_list = Seat.objects.all().order_by('room')
    return {'seat_list':seat_list,'online_users':online_users}
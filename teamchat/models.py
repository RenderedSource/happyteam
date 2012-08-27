from django.contrib.auth.models import User
from django.db import models



class Room(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

class UserRoom(models.Model):
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room, related_name="users", blank=True, null=True)
    session = models.CharField(max_length=30)


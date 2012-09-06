from django.db import models

class CalendarEvent(models.Model):
    title  = models.CharField(max_length=60)
    allDay = models.BooleanField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    url = models.URLField(blank=True)
    class_name = models.CharField(max_length=60, blank=True)
    editable = models.BooleanField(default=False)
    #style settings 1.5 version
    color= models.CharField(max_length=10, blank=True)
    background_color= models.CharField(max_length=10, blank=True)
    border_color= models.CharField(max_length=10, blank=True)
    text_color= models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return self.title

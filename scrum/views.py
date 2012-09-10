# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from scrum.models import Story, StoryStatus

def story_desc(request):
    story_list = Story.objects.all()
    status_list = StoryStatus.objects.all().order_by('sort')
    return render_to_response('scrum/story_desc.html',
            {
            'story_list': story_list,
            'status_list': status_list
        },
        context_instance=RequestContext(request))

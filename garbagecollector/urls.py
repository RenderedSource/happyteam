from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'garbagecollector.views.index'),
    url(r'^addlooser/', 'garbagecollector.views.add_looser', name='add_looser'),
    url(r'^get-online/', 'garbagecollector.views.get_online', name='get_online')
)
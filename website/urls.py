from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'website.views.Index'),
    url('^markdown/', include( 'django_markdown.urls')),
    url('^news/', include( 'importantnews.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^login/$', 'website.views.login', name='login'),
    url(r'^login-begin/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', }, name='logout'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', }, name='logout'),
    url(r'^merge/', include('mergemaster.urls')),
    url(r'^gc/', include('garbagecollector.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

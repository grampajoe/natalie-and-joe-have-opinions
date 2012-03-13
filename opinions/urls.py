from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'opinions.views.index', name='index'),
    url(r'^(?P<thing_slug>[\w-]+)/$', 'opinions.views.thing', name='thing'),
    url(r'^(?P<slug1>[\w-]+)/(?P<slug2>[\w-]+)/',
        'opinions.views.versus', name='versus'),
)

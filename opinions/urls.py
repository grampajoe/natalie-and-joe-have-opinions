from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'opinions.views.thing', name='index'),
    url(r'^(?P<thing_slug>[\w-]+)$', 'opinions.views.thing', name='thing'),
)

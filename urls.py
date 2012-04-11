from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'opinions.views.home', name='home'),
    url(r'^things/', include('opinions.urls')),
    url(r'^search/(.*)$', 'opinions.views.search', name='search'),
    url(r'^search$', 'opinions.views.search', name='search_blank'),
    
    url(r'autocomplete/(.*)$', 'opinions.views.autocomplete', name='autocomplete'),

    url(r'^tightpagecya/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

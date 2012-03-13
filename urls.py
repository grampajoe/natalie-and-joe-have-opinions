from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'opinions.views.home', name='home'),
    url(r'^things/', include('opinions.urls')),
    url(r'^search/(.*)$', 'opinions.views.search', name='search'),
    url(r'^search$', 'opinions.views.search', name='search_blank'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

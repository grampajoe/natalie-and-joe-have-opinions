from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'natalieandjoe.opinions.views.home', name='home'),
    url(r'^opinions/', include('natalieandjoe.opinions.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

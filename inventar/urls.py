from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from inventory.views import home
from inventory.views import item
from inventory.views import search
from inventory.views import graph

urlpatterns = patterns('',
    url(r'^$', home, name='home'),

    url(r'^item/(?P<selectedid>[0-9A-Za-z]{4})/$', item, name='item'),
    url(r'^search/(?P<term>[^/]+)/$', search, name='search'),
    url(r'^graph/$', graph, name='graph'),

    url(r'^admin/', include(admin.site.urls)),
)

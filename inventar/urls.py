from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from inventory.views import home
from inventory.views import item
from inventory.views import search
from inventory.views import graph
from inventory.views import stats
from inventory.views import upload

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    #(r'^openid/', include('django_openid_auth.urls')),

    url(r'^item/(?P<selectedid>[0-9A-Za-z]{4})/$', item, name='item'),
    url(r'^search/(?P<term>[^/]+)/$', search, name='search'),
    url(r'^graph/$', graph, name='graph'),
    url(r'^stats/$', stats, name='stats'),
    url(r'^upload/$', upload, name='upload'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

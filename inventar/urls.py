# Copyright (c) 2012-2013 Sebastian Reichel <sre@ring0.de>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from inventory.views import home
from inventory.views import item
from inventory.views import search
from inventory.views import graph
from inventory.views import stats

urlpatterns = patterns('',
    url(r'^$', home, name='home'),

    (r'^openid/', include('django_openid_auth.urls')),

    url(r'^item/(?P<selectedid>[0-9A-Za-z]{4})/$', item, name='item'),
    url(r'^search/(?P<term>[^/]+)/$', search, name='search'),
    url(r'^graph/$', graph, name='graph'),
    url(r'^stats/$', stats, name='stats'),

    url(r'^admin/', include(admin.site.urls)),
)

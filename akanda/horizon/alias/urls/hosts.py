from django.conf.urls.defaults import patterns, url

from akanda.horizon.alias.views import (
    CreateHostAliasView, EditHostAliasView)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateHostAliasView.as_view(), name='create'),
    url(r'^(?P<host_alias_id>[^/]+)/edit/$', EditHostAliasView.as_view(),
        name='edit'),
)

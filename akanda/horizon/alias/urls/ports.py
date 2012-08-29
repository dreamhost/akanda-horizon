from django.conf.urls.defaults import patterns, url

from akanda.horizon.alias.views import (
    CreatePortAliasView, EditPortAliasView)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreatePortAliasView.as_view(), name='create'),
    url(r'^(?P<port_alias_id>[^/]+)/edit/$', EditPortAliasView.as_view(),
        name='edit'),
)

from django.conf.urls.defaults import patterns, url

from akanda.horizon.alias.views import (
    CreateNetworkView, EditNetworkAliasView)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateNetworkView.as_view(), name='create'),
    url(r'^(?P<network_alias_id>[^/]+)/edit/$', EditNetworkAliasView.as_view(),
        name='edit'),
)

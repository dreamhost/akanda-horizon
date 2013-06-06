from django.conf.urls.defaults import patterns, url

from akanda.horizon.network_topology.views import JSONView


urlpatterns = patterns(
    '',
    url(r'json/$', JSONView.as_view(), name='json'),
)

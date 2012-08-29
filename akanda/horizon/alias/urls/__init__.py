from django.conf.urls.defaults import patterns, url, include

from akanda.horizon.alias.urls import ports, hosts, networks


urlpatterns = patterns(
    '',
    url(r'ports/', include(ports, namespace='ports')),
    url(r'hosts/', include(hosts, namespace='hosts')),
    url(r'networks/', include(networks, namespace='networks')),
)

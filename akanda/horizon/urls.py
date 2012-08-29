from django.conf.urls.defaults import patterns, url, include

from .views import IndexView

from akanda.horizon.alias import urls as alias_urls
from akanda.horizon.firewall import urls as firewall_urls
from akanda.horizon.portforwarding import urls as forwarding_rules


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'alias/', include(alias_urls, namespace='alias'),),
    url(r'firewall/', include(firewall_urls, namespace='firewall'),),
    url(r'forwarding/', include(forwarding_rules, namespace='forwarding'),),
)

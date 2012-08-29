from django.conf.urls.defaults import patterns, url

from akanda.horizon.firewall.views import (
    CreateFirewallRuleView, EditFirewallRuleView)

urlpatterns = patterns(
    '',
    url(r'create/$', CreateFirewallRuleView.as_view(), name='create'),
    url(r'^(?P<firewall_rule_id>[^/]+)/edit/$', EditFirewallRuleView.as_view(),
        name='edit'),
)

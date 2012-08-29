from django.conf.urls.defaults import patterns, url

from akanda.horizon.portforwarding.views import (
    CreatePortForwardingRuleView, EditPortForwardingRuleView)

urlpatterns = patterns(
    '',
    url(r'^create/$', CreatePortForwardingRuleView.as_view(), name='create'),
    url(r'^(?P<portforward_rule_id>[^/]+)/edit/$',
        EditPortForwardingRuleView.as_view(), name='edit'),
)

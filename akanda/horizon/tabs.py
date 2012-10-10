from django.utils.translation import ugettext as _

from horizon import tabs

from akanda.horizon.alias.tabs import AliasTab
from akanda.horizon.configuration.tabs import ConfigurationTab
from akanda.horizon.firewall.tabs import FirewallRuleTab
from akanda.horizon.portforwarding.tabs import PortForwardingTab


# class NatTab(tabs.Tab):
#     name = _("Nat")
#     slug = "nat"
#     template_name = "akanda/simple.html"
#
#     def get_context_data(self, request):
#         return {}
#
#
# class VPNTab(tabs.Tab):
#     name = _("VPN")
#     slug = "vpn"
#     template_name = "akanda/simple.html"
#
#     def get_context_data(self, request):
#         return {}


class NetworkingTabs(tabs.TabGroup):
    slug = "networkingtabs"
    tabs = (AliasTab,
            ConfigurationTab,
            FirewallRuleTab,
            #NatTab,
            PortForwardingTab,
            #VPNTab,
            )


def alias_tab_redirect():
    tab_group_slug = NetworkingTabs.slug
    tab_slug = AliasTab.slug
    return "%s__%s" % (tab_group_slug, tab_slug)


def configuration_tab_redirect():
    tab_group_slug = NetworkingTabs.slug
    tab_slug = ConfigurationTab.slug
    return "%s__%s" % (tab_group_slug, tab_slug)


def firewall_tab_redirect():
    tab_group_slug = NetworkingTabs.slug
    tab_slug = FirewallRuleTab.slug
    return "%s__%s" % (tab_group_slug, tab_slug)


def portforwarding_tab_redirect():
    tab_group_slug = NetworkingTabs.slug
    tab_slug = PortForwardingTab.slug
    return "%s__%s" % (tab_group_slug, tab_slug)

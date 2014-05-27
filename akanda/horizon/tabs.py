# Copyright 2014 DreamHost, LLC 
#
# Author: DreamHost, LLC 
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


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

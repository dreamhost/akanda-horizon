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


from django.utils.translation import ugettext as _

from horizon import tabs

from akanda.horizon.api import neutron_extensions_client
from akanda.horizon.alias.tables import (
    PortAliasTable, HostAliasTable, NetworkAliasTable)


class AliasTab(tabs.TableTab):
    name = _("Alias")
    slug = "alias_tab"
    table_classes = (PortAliasTable, HostAliasTable, NetworkAliasTable)
    template_name = "akanda/alias/index.html"
    # preload = False

    def get_ports_data(self):
        return neutron_extensions_client.portalias_list(self.request)

    def get_hosts_data(self):
        return neutron_extensions_client.addressgroup_list(self.request)

    def get_networks_data(self):
        return neutron_extensions_client.networkalias_list(self.request)

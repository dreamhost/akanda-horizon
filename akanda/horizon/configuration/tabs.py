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


import collections

from django.utils.translation import ugettext as _

from openstack_dashboard.api import neutron
from horizon import tabs

from akanda.horizon.configuration.tables.publicips import PublicIPsTable


# The table rendering code assumes it is getting an
# object with an "id" property and other properties
# based on the column definitions for the table.
# This is a light-weight data structure that looks
# like what we need for the publicips table.
PublicIP = collections.namedtuple('PublicIP', 'id router_name ipaddr')


class ConfigurationTab(tabs.TableTab):
    """Tab to show the user generic configuration settings.
    """
    name = _("Configuration")
    slug = "configuration_tab"
    template_name = "akanda/configuration/index.html"
    table_classes = (PublicIPsTable,)

    def get_publicips_data(self):
        data = []
        for router in neutron.router_list(
                self.request, tenant_id=self.request.user.tenant_id):
            router_info = neutron.router_get(self.request, router.id)
            for port in router_info.get('ports', []):
                if port.get('device_owner') != 'network:router_gateway':
                    continue
                ips = [i['ip_address'] for i in port.get('fixed_ips', [])]
                data.append(PublicIP(None, router.get('name'), ips))
        return data

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


from mock import patch

from django.core.urlresolvers import reverse
from openstack_dashboard.test import helpers

from akanda.horizon import alias  # noqa


class TestRoutersView(helpers.TestCase):

    @patch('openstack_dashboard.api.neutron.port_list')
    @patch('openstack_dashboard.api.neutron.network_list')
    @patch('openstack_dashboard.api.neutron.network_get')
    @patch('openstack_dashboard.api.neutron.router_get')
    def test_get_interfaces_data(self, router_get, network_get, network_list,
                                 port_list):
        ports = [{
            'status': 'ACTIVE',
            'device_owner': 'network:router_interface',
            'admin_state': 'UP',
            'fixed_ips': [],
            'id': '063cf7f3-ded1-4297-bc4c-31eae876cc91',
            'device_id': 'af75c8e5-a1cc-4567-8d04-44fcd6922890',
            'name': '',
            'admin_state_up': True,
            'network_id': '82288d84-e0a5-42ac-95be-e6af08727e42',
            'tenant_id': '1',
            'mac_address': 'fa:16:3e:9c:d5:7e'
        }, {
            'status': 'ACTIVE',
            'device_owner': 'network:router_gateway',  # FILTER THIS OUT
            'admin_state': 'UP',
            'fixed_ips': [],
            'id': '063cf7f3-ded1-4297-bc4c-31eae876cc92',
            'device_id': 'af75c8e5-a1cc-4567-8d04-44fcd6922891',
            'name': '',
            'admin_state_up': True,
            'network_id': '82288d84-e0a5-42ac-95be-e6af08727e42',
            'tenant_id': '1',
            'mac_address': 'fa:16:3e:9c:d5:7f'
        }, {
            'status': 'ACTIVE',
            'device_owner': 'network:router_management',  # FILTER THIS OUT
            'admin_state': 'UP',
            'fixed_ips': [],
            'id': '063cf7f3-ded1-4297-bc4c-31eae876cc93',
            'device_id': 'af75c8e5-a1cc-4567-8d04-44fcd6922892',
            'name': '',
            'admin_state_up': True,
            'network_id': '82288d84-e0a5-42ac-95be-e6af08727e42',
            'tenant_id': '1',
            'mac_address': 'fa:16:3e:9c:d5:7d'
        }]
        network_list.return_value = [
            n for n in self.networks.list() if n['router:external']
        ]
        network_get.return_value = self.networks.list()[2]
        router_get.return_value = self.routers.first()
        port_list.return_value = ports
        router_get.return_value.ports = ports

        url = reverse('horizon:project:routers:detail', args=('abc123',))
        res = self.client.get(url)

        self.assertTemplateUsed(res, 'project/routers/detail.html')
        ports = res.context['interfaces_table'].data
        assert len(ports) == 1

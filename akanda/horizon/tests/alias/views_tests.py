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


from django.contrib.messages.storage import default_storage
from django.core.urlresolvers import reverse

from mock import patch

from openstack_dashboard.test import helpers

from akanda.horizon.tabs import alias_tab_redirect
from akanda.horizon import alias  # noqa


class TestNetworkAliasView(helpers.TestCase):

    def setUp(self):
        super(TestNetworkAliasView, self).setUp()
        # mock this method because both the network forms use it to fill
        # the drop-down menu for the group field in the html template
        self.form_data = {'name': 'net1', 'cidr': '192.168.1.1', 'group': 1}
        self.get_address_groups = patch(
            'akanda.horizon.alias.forms.networks.get_address_groups',
            lambda x: [(1, 'group')])
        self.get_address_groups.start()
        self.neutron_extensions_client = patch(
            'akanda.horizon.alias.forms.networks.neutron_extensions_client')
        self.neutron_extensions_client.start()

    def tearDown(self):
        self.get_address_groups.stop()
        self.neutron_extensions_client.stop()

    def test_create_network_alias(self):
        url = reverse('horizon:project:networking:alias:networks:create')
        response = self.client.post(url, self.form_data)
        self.assertNoFormErrors(response)

    def test_create_network_alias_redirect(self):
        url = reverse('horizon:project:networking:alias:networks:create')
        response = self.client.post(url, self.form_data)
        redirect_url = "%s?tab=%s" % (
            reverse('horizon:project:networking:index'), alias_tab_redirect())
        self.assertRedirectsNoFollow(response, redirect_url)

    def test_create_network_alias_assert_template(self):
        url = reverse('horizon:project:networking:alias:networks:create')
        response = self.client.post(url)
        self.assertTemplateUsed(response, 'akanda/alias/networks/create.html')

    def test_create_network_alias_message(self):
        url = reverse('horizon:project:networking:alias:networks:create')
        response = self.client.post(url, self.form_data)
        storage = default_storage(response.request)
        message_cookie = response.cookies['messages'].value
        messages = [m.message for m in storage._decode(message_cookie)]
        msg = "Successfully created network alias: %s"
        self.assertIn(msg % self.form_data['name'], messages)
        self.assertMessageCount(success=1)

    @patch('alias.views.networks.neutron_extensions_client.networkalias_get')
    def test_update_network_alias(self, get_obj):
        url = reverse(
            'horizon:project:networking:alias:networks:edit', args=['1'])
        network_ref = {'name': 'net1', 'cidr': '192.168.1.1',
                       'groups': 1, 'id': 1}
        get_obj.return_value = network_ref
        response = self.client.post(url)
        self.assertItemsEqual(
            response.context['network_alias'], network_ref)

    @patch('alias.views.networks.neutron_extensions_client.networkalias_get')
    def test_update_network_alias_assert_template(self, get_obj):
        url = reverse(
            'horizon:project:networking:alias:networks:edit', args=['1'])
        network_ref = {'name': 'net1', 'cidr': '192.168.1.1',
                       'groups': 1, 'id': 1}
        get_obj.return_value = network_ref
        response = self.client.post(url)
        self.assertTemplateUsed(
            response, 'akanda/alias/networks/edit_rules.html')

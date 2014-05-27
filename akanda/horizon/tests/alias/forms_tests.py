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

from openstack_dashboard.test import helpers

from akanda.horizon.alias.forms import (
    CreatePortAliasForm, EditPortAliasForm,
    CreateNetworkAliasForm, EditNetworkAliasForm)
from akanda.horizon.tests.base.forms import AliasFormTest


class TestPortAliasForm(helpers.TestCase, AliasFormTest):

    def setUp(self):
        super(TestPortAliasForm, self).setUp()
        self.form_data = {'alias_name': 'SSH', 'protocol': 'tcp', 'port': 123}

    def test_create_port_alias(self):
        self._create_or_update_alias(CreatePortAliasForm,
                                     '_create_port_alias',
                                     "Successfully created port alias",
                                     'alias_name')

    def test_create_port_alias_fail(self):
        self._create_or_update_alias_fail(CreatePortAliasForm,
                                          '_create_port_alias',
                                          "Unable to create port alias.")

    def test_update_port_alias(self):
        self._create_or_update_alias(EditPortAliasForm,
                                     '_update_port_alias',
                                     "Successfully updated port alias",
                                     'alias_name')

    def test_update_port_alias_fail(self):
        self._create_or_update_alias_fail(EditPortAliasForm,
                                          '_update_port_alias',
                                          "Unable to edit port alias.")


class TestNetworkAliasForm(helpers.TestCase, AliasFormTest):

    def setUp(self):
        super(TestNetworkAliasForm, self).setUp()
        self.form_data = {'name': 'net1', 'cidr': '192.168.1.1', 'group': 1}
        # mock this method because both the network forms use it to fill
        # the drop-down menu for the group field in the html template
        self.get_address_groups = patch(
            'akanda.horizon.alias.forms.networks.get_address_groups',
            lambda x: [(1, 'group')])
        self.get_address_groups.start()

    def tearDown(self):
        self.get_address_groups.stop()

    def test_create_network_alias(self):
        self._create_or_update_alias(CreateNetworkAliasForm,
                                     '_create_network_alias',
                                     "Successfully created network alias",
                                     'name')

    def test_create_network_alias_fail(self):
        self._create_or_update_alias_fail(CreateNetworkAliasForm,
                                          '_create_network_alias',
                                          "Unable to create network alias.")

    def test_update_network_alias(self):
        self._create_or_update_alias(EditNetworkAliasForm,
                                     '_update_network_alias',
                                     "Successfully updated network alias",
                                     'name')

    def test_update_network_alias_fail(self):
        self._create_or_update_alias_fail(EditNetworkAliasForm,
                                          '_update_network_alias',
                                          "Unable to update network alias.")

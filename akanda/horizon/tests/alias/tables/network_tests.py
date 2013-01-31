# -*- encoding: utf-8 -*-
#
# Copyright © 2012 New Dream Network, LLC (DreamHost)
#
# Author: Rosario Di Somma <rosario.disomma@dreamhost.com>
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

from mock import patch, DEFAULT

from horizon import test

from akanda.horizon.alias.tables import NetworkAliasTable
from akanda.horizon.api.quantum_extensions_client import Network
from akanda.horizon.tests.base import table


NETWORK_TEST_DATA = (
    Network('net1', '192.168.1.1', '1'),
    Network('net2', '192.168.1.2', '2'),
    Network('net3', '192.168.1.3', '3'),
)


class TestNetworkAliasTableInstantiation(test.TestCase,
                                         table.TableInstantiationTests):

    def setUp(self):
        super(TestNetworkAliasTableInstantiation, self).setUp()
        self.data = NETWORK_TEST_DATA
        self.table = NetworkAliasTable(self.request, self.data)

    def test_name_property(self):
        self._name_property("networks")

    def test_verbose_name(self):
        self._verbose_name(u"Network Aliases")

    def test_table_columns(self):
        self._table_columns(['multi_select', 'alias_name', 'cidr', 'actions'])


class TestNetworkAliasTableConstruction(test.TestCase,
                                        table.TableConstructionTests):
    def setUp(self):
        super(TestNetworkAliasTableConstruction, self).setUp()
        self.data = NETWORK_TEST_DATA
        self.table = NetworkAliasTable(self.request, self.data)

    def test_table_columns_construction(self):
        self._table_columns_construction(['multi_select', 'alias_name',
                                          'cidr', 'actions'])

    def test_row_cells_construction(self):
        self._row_cells_construction(['multi_select', 'alias_name',
                                      'cidr', 'actions'])


class TestNetworkAliasTableActionsVerboseName(
        test.TestCase, table.TableActionsVerboseNameTests):

    def setUp(self):
        super(TestNetworkAliasTableActionsVerboseName, self).setUp()
        request = self.factory.post('/my_url/')
        self.data = NETWORK_TEST_DATA
        self.table = NetworkAliasTable(request, self.data)
        self.table_actions = self.table.get_table_actions()

    def test_create_actions_verbose_name(self):
        self._check_actions_verbose_name('verbose_name', 'Create Alias')

    def test_delete_actions_verbose_name(self):
        self._check_actions_verbose_name('verbose_name', 'Delete Network')

    def test_delete_actions_verbose_plural_name(self):
        self._check_actions_verbose_name('verbose_plural_name',
                                         'Delete Networks')

    def test_delete_actions_present_name(self):
        self._check_actions_verbose_name('action_present', 'Delete')

    def test_delete_actions_past_name(self):
        self._check_actions_verbose_name('action_past', 'Deleted')

    def test_edit_action_verbose_name(self):
        self._check_actions_verbose_name('verbose_name', 'Edit Alias')


class TestNetworkAliasTableRendering(test.TestCase, table.TableRenderingTests):

    def setUp(self):
        super(TestNetworkAliasTableRendering, self).setUp()
        self.data = NETWORK_TEST_DATA
        self.table = NetworkAliasTable(self.request, self.data)


class TestNetworkAliasTableAction(test.TestCase):

    def test_delete_actions_post(self):
        action_string = "networks__delete"
        req = self.factory.post('/my_url/',
                                {'action': action_string,
                                 'object_ids': [1, 2]})
        self.table = NetworkAliasTable(req, NETWORK_TEST_DATA)
        table_actions = self.table.get_table_actions()
        delete_action = table_actions[1]

        with patch.multiple(delete_action, delete=DEFAULT,
                            success_url=DEFAULT) as values:
            values['delete'].return_value = None
            values['mock_success.return_value'] = ''
            handled = self.table.maybe_handle()
            self.assertEqual(handled.status_code, 302)
            self.assertEqual(list(req._messages)[0].message,
                             u"Deleted Networks: net1, net2")

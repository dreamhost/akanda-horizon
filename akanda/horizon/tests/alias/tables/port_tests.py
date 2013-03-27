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

from openstack_dashboard.test import helpers

from akanda.horizon.alias.tables import PortAliasTable
from akanda.horizon.api.quantum_extensions_client import Port
from akanda.horizon.tests.base import table

PORT_TEST_DATA = (
    Port('SSH', 'tcp', 22, '1'),
    Port('IRC', 'tcp', 33, '2'),
    Port('MySQL', 'udp', 44, '3'),
)


class TestPortAliasTableInstantiation(helpers.TestCase,
                                      table.TableInstantiationTests):

    def setUp(self):
        super(TestPortAliasTableInstantiation, self).setUp()
        self.data = PORT_TEST_DATA
        self.table = PortAliasTable(self.request, self.data)

    def test_name_property(self):
        self._name_property("ports")

    def test_verbose_name(self):
        self._verbose_name(u"Port Aliases")

    def test_table_columns(self):
        self._table_columns(['multi_select', 'alias_name',
                             'protocol', 'ports', 'actions'])


class TestPortAliasTableConstruction(helpers.TestCase,
                                     table.TableConstructionTests):
    def setUp(self):
        super(TestPortAliasTableConstruction, self).setUp()
        self.data = PORT_TEST_DATA
        self.table = PortAliasTable(self.request, self.data)

    def test_table_columns_construction(self):
        self._table_columns_construction(['multi_select', 'alias_name',
                                          'protocol', 'ports', 'actions'])

    def test_row_cells_construction(self):
        self._row_cells_construction(['multi_select', 'alias_name',
                                      'protocol', 'ports', 'actions'])


class TestPortAliasTableActionsVerboseName(
        helpers.TestCase, table.TableActionsVerboseNameTests):

    def setUp(self):
        super(TestPortAliasTableActionsVerboseName, self).setUp()
        request = self.factory.post('/my_url/')
        self.data = PORT_TEST_DATA
        self.table = PortAliasTable(request, self.data)
        self.table_actions = self.table.get_table_actions()

    def test_create_actions_verbose_name(self):
        self._check_actions_verbose_name('verbose_name', 'Create Alias')

    def test_delete_actions_verbose_name(self):
        self._check_actions_verbose_name('verbose_name', 'Delete Port Alias')

    def test_delete_actions_verbose_plural_name(self):
        self._check_actions_verbose_name('verbose_plural_name',
                                         'Delete Port Aliases')

    def test_delete_actions_present_name(self):
        self._check_actions_verbose_name('action_present', 'Delete')

    def test_delete_actions_past_name(self):
        self._check_actions_verbose_name('action_past', 'Deleted')

    def test_edit_action_verbose_name(self):
        self._check_actions_verbose_name('verbose_name', 'Edit Alias')


class TestPortAliasTableRendering(helpers.TestCase, table.TableRenderingTests):

    def setUp(self):
        super(TestPortAliasTableRendering, self).setUp()
        self.data = PORT_TEST_DATA
        self.table = PortAliasTable(self.request, self.data)


class TestPortAliasTableAction(helpers.TestCase):

    def test_delete_actions_post(self):
        action_string = "ports__delete"
        req = self.factory.post('/my_url/',
                                {'action': action_string,
                                 'object_ids': [1, 2]})
        self.table = PortAliasTable(req, PORT_TEST_DATA)
        table_actions = self.table.get_table_actions()
        delete_action = table_actions[1]

        with patch.multiple(delete_action, delete=DEFAULT,
                            success_url=DEFAULT) as values:
            values['delete'].return_value = None
            values['mock_success.return_value'] = ''
            handled = self.table.maybe_handle()
            self.assertEqual(handled.status_code, 302)
            self.assertEqual(list(req._messages)[0].message,
                             u"Deleted Port Aliases: SSH, IRC")

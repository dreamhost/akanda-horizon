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

from django import http
from mock import patch, DEFAULT

from horizon import test

from akanda.horizon.alias.tables import PortAliasTable
from akanda.horizon.api.quantum_extensions_client import (Port)

PORT_TEST_DATA = (
    Port('SSH', 'tcp', 22, '1'),
    Port('IRC', 'tcp', 33, '2'),
    Port('MySQL', 'udp', 44, '3'),
)


class TestPortAliasTableInstantiation(test.TestCase):

    def setUp(self):
        super(TestPortAliasTableInstantiation, self).setUp()
        self.table = PortAliasTable(self.request, PORT_TEST_DATA)

    def test_data_property(self):
        """ Tests everything that happens when the table is instantiated. """
        # Test data property defined on the table
        self.assertEqual(self.table.data, PORT_TEST_DATA)

    def test_name_property(self):
        # Test name property defined on the table
        self.assertEqual(self.table.name, "ports")

    def test_action_column_options(self):
        # Verify calculated options that weren't specified explicitly
        self.assertTrue(self.table._meta.actions_column)

    def test_multi_select_options(self):
        # Verify calculated options that weren't specified explicitly
        self.assertTrue(self.table._meta.multi_select)

    def test_verbose_name(self):
        # Test for verbose_name
        self.assertEqual(unicode(self.table), u"Port Aliases")

    def test_table_columns(self):
        # Test column ordering and exclusion.
        # This should include multi_select and actions but should not contain
        # the excluded column.
        self.assertQuerysetEqual(self.table.columns.values(),
                                 ['<Column: multi_select>',
                                  '<Column: alias_name>',
                                  '<Column: protocol>',
                                  '<Column: ports>',
                                  '<Column: actions>'])

    def test_table_base_actions(self):
        # Test base actions (these also test ordering)
        self.assertQuerysetEqual(self.table.base_actions.values(),
                                 ['<Create: create>',
                                  '<Delete: delete>',
                                  '<Edit: edit>'])

    def test_table_actions(self):
        # Test table actions (these also test ordering)
        self.assertQuerysetEqual(self.table.get_table_actions(),
                                 ['<Create: create>',
                                  '<Delete: delete>'])

    def test_row_actions(self):
        # Test row actions (these also test ordering)
        self.assertQuerysetEqual(self.table.get_row_actions(PORT_TEST_DATA[0]),
                                 ['<Edit: edit>'])

    def test_multi_select_column_properties(self):
        # Test auto-generated columns
        multi_select = self.table.columns['multi_select']
        self.assertEqual(multi_select.auto, "multi_select")
        self.assertEqual(multi_select.get_final_attrs().get('class', ""),
                         "multi_select_column")

    def test_actions_column_properties(self):
        # Test auto-generated columns
        actions = self.table.columns['actions']
        self.assertEqual(actions.auto, "actions")
        self.assertEqual(actions.get_final_attrs().get('class', ""),
                         "actions_column")


class TestPortAliasTableConstruction(test.TestCase):

    def setUp(self):
        super(TestPortAliasTableConstruction, self).setUp()
        self.table = PortAliasTable(self.request, PORT_TEST_DATA)

    def test_table_columns_construction(self):
        # Verify we retrieve the right columns for headers
        columns = self.table.get_columns()
        self.assertQuerysetEqual(columns, ['<Column: multi_select>',
                                           '<Column: alias_name>',
                                           '<Column: protocol>',
                                           '<Column: ports>',
                                           '<Column: actions>'])

    def test_rows_construction(self):
        # Verify we retrieve the right rows from our data
        rows = self.table.get_rows()
        self.assertQuerysetEqual(rows, ['<Row: ports__row__1>',
                                        '<Row: ports__row__2>',
                                        '<Row: ports__row__3>'])

    def test_row_cells_construction(self):
        # Verify each row contains the right cells
        rows = self.table.get_rows()
        self.assertQuerysetEqual(rows[0].get_cells(),
                                 ['<Cell: multi_select, ports__row__1>',
                                  '<Cell: alias_name, ports__row__1>',
                                  '<Cell: protocol, ports__row__1>',
                                  '<Cell: ports, ports__row__1>',
                                  '<Cell: actions, ports__row__1>'])


class TestPortAliasTableActionVerboseName(test.TestCase):

    def setUp(self):
        super(TestPortAliasTableActionVerboseName, self).setUp()
        request = self.factory.post('/my_url/')
        self.table = PortAliasTable(request, PORT_TEST_DATA)
        self.table_actions = self.table.get_table_actions()

    def test_create_actions_verbose_name(self):
        create_action = self.table_actions[0]
        self.assertEqual(unicode(create_action.verbose_name), 'Create Alias')

    def test_delete_actions_verbose_name(self):
        delete_action = self.table_actions[1]
        self.assertEqual(unicode(delete_action.verbose_name),
                         'Delete Port Alias')

    def test_delete_actions_verbose_plural_name(self):
        delete_action = self.table_actions[1]
        self.assertEqual(unicode(delete_action.verbose_name_plural),
                         'Delete Port Aliases')

    def test_delete_actions_present_name(self):
        delete_action = self.table_actions[1]
        self.assertEqual(unicode(delete_action.action_present), 'Delete')

    def test_delete_actions_past_name(self):
        delete_action = self.table_actions[1]
        self.assertEqual(unicode(delete_action.action_past), 'Deleted')

    def test_edit_action_verbose_name(self):
        row_actions = self.table.get_row_actions(PORT_TEST_DATA[0])
        edit_action = row_actions[0]
        self.assertEqual(unicode(edit_action.verbose_name), 'Edit Alias')


class TestPortAliasTableRendering(test.TestCase):

    def setUp(self):
        super(TestPortAliasTableRendering, self).setUp()
        self.table = PortAliasTable(self.request, PORT_TEST_DATA)

    def test_table_actions_rendering(self):
        table_actions = self.table.render_table_actions()
        response = http.HttpResponse(table_actions)
        self.assertContains(response, 'id="ports__action_create"', 1)
        self.assertContains(response, 'ajax-modal btn-create"', 1)
        self.assertContains(response, '<button  id="ports__action_delete"', 1)
        self.assertContains(response, 'ports__delete', 1)

    def test_row_actions_rendering(self):
        row_actions = self.table.render_row_actions(PORT_TEST_DATA[0])
        response = http.HttpResponse(row_actions)
        self.assertContains(response, "<a", 1)
        self.assertContains(response, "ajax-modal", 1)
        self.assertContains(response, 'id="ports__row_1__action_edit"', 1)

    def test_whole_table_rendering(self):
        table = self.table.render()
        response = http.HttpResponse(table)
        self.assertContains(response, '<table id="ports"')
        self.assertContains(response, '<th ', 6)
        self.assertContains(response, 'id="ports__row__1"')
        self.assertContains(response, 'id="ports__row__2"')
        self.assertContains(response, 'id="ports__row__3"')


class TestTableAction(test.TestCase):

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

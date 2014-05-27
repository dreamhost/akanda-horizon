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

from django import http


def format_cols(values):
    msg = '<Column: %s>'
    return [msg % value for value in values]


def format_cells(values, table_name):
    msg = '<Cell: %s, ' + table_name + '__row__1>'
    return [msg % value for value in values]


def format_rows(len, table_name):
    msg = '<Row: ' + table_name + '__row__%d>'
    return [msg % (i + 1) for i in range(len)]


class TableInstantiationTests(object):
    """ Tests everything that happens when the table is instantiated. """

    def _name_property(self, name):
        # Test name property defined on the table
        self.assertEqual(self.table.name, name)

    def _verbose_name(self, verbose_name):
        # Test for verbose_name
        self.assertEqual(unicode(self.table), verbose_name)

    def _table_columns(self, expected):
        # Test column ordering and exclusion.
        # This should include multi_select and actions but should not contain
        # the excluded column.
        expected = format_cols(expected)
        self.assertQuerysetEqual(self.table.columns.values(), expected)

    def test_data_property(self):
        # Test data property defined on the table
        self.assertEqual(self.table.data, self.data)

    def test_action_column_options(self):
        # Verify calculated options that weren't specified explicitly
        self.assertTrue(self.table._meta.actions_column)

    def test_multi_select_options(self):
        # Verify calculated options that weren't specified explicitly
        self.assertTrue(self.table._meta.multi_select)

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
        self.assertQuerysetEqual(self.table.get_row_actions(self.data[0]),
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


class TableConstructionTests(object):
    """Test everything happens after the table is been instatiated"""

    def _table_columns_construction(self, expected):
        # Verify we retrieve the right columns for headers
        columns = self.table.get_columns()
        expected = format_cols(expected)
        self.assertQuerysetEqual(columns, expected)

    def _row_cells_construction(self, expected):
        # Verify each row contains the right cells
        rows = self.table.get_rows()
        expected = format_cells(expected, self.table.name)
        self.assertQuerysetEqual(rows[0].get_cells(), expected)

    def test_rows_construction(self):
        # Verify we retrieve the right rows from our data
        rows = self.table.get_rows()
        expected = format_rows(len(rows), self.table.name)
        self.assertQuerysetEqual(rows, expected)


class TableActionsVerboseNameTests(object):
    """ Test names and messages"""

    def _check_actions_verbose_name(self, attr_name, value):
        result = False
        for action in self.table_actions:
            if unicode(getattr(action, attr_name, '') == value):
                result = True
                break
        self.assertTrue(result)


class TableRenderingTests(object):
    """ Test table rendering"""

    def test_table_actions_rendering(self):
        table_actions = self.table.render_table_actions()
        response = http.HttpResponse(table_actions)
        self.assertContains(
            response, 'id="%s__action_create"' % self.table.name, 1)
        self.assertContains(response, 'ajax-modal btn-create"', 1)
        self.assertContains(
            response, 'id="%s__action_delete"' % self.table.name, 1)
        self.assertContains(response, '%s__delete' % self.table.name, 1)

    def test_row_actions_rendering(self):
        row_actions = self.table.render_row_actions(self.data[0])
        response = http.HttpResponse(row_actions)
        self.assertContains(response, "<a", 1)
        self.assertContains(response, "ajax-modal", 1)
        self.assertContains(
            response, 'id="%s__row_1__action_edit"' % self.table.name, 1)

    def test_whole_table_rendering(self):
        table = self.table.render()
        response = http.HttpResponse(table)
        self.assertContains(response, '<table id="%s"' % self.table.name, 1)

        # check cells number
        rows = self.table.get_rows()
        cells = rows[0].get_cells()
        self.assertContains(response, '<th ', len(cells) + 1)

        # check rows
        for i in range(1, len(rows) + 1):
            self.assertContains(
                response, 'id="%s__row__%d"' % (self.table.name, i), 1)

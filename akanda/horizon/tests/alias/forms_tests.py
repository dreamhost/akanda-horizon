from horizon import test

from akanda.horizon.alias.forms import CreatePortAliasForm, EditPortAliasForm
from akanda.horizon.tests.base.forms import AliasFormTest


class TestPortAliasForm(test.TestCase, AliasFormTest):

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

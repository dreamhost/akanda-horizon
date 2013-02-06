from django.contrib.messages.storage import default_storage
from django.core.urlresolvers import reverse

from mock import patch

from horizon import test

from akanda.horizon.tabs import alias_tab_redirect
from akanda.horizon import alias  # noqa


class TestNetworkAliasView(test.TestCase):

    def setUp(self):
        super(TestNetworkAliasView, self).setUp()
        # mock this method because both the network forms use it to fill
        # the drop-down menu for the group field in the html template
        self.form_data = {'name': 'net1', 'cidr': '192.168.1.1', 'group': 1}
        self.get_address_groups = patch(
            'akanda.horizon.alias.forms.networks.get_address_groups',
            lambda x: [(1, 'group')])
        self.get_address_groups.start()
        self.quantum_extensions_client = patch(
            'akanda.horizon.alias.forms.networks.quantum_extensions_client')
        self.quantum_extensions_client.start()

    def tearDown(self):
        self.get_address_groups.stop()
        self.quantum_extensions_client.stop()

    def test_create_network_alias(self):
        url = reverse('horizon:nova:networking:alias:networks:create')
        response = self.client.post(url, self.form_data)
        self.assertNoFormErrors(response)

    def test_create_network_alias_redirect(self):
        url = reverse('horizon:nova:networking:alias:networks:create')
        response = self.client.post(url, self.form_data)
        redirect_url = "%s?tab=%s" % (reverse('horizon:nova:networking:index'),
                                      alias_tab_redirect())
        self.assertRedirectsNoFollow(response, redirect_url)

    def test_create_network_alias_assert_template(self):
        url = reverse('horizon:nova:networking:alias:networks:create')
        response = self.client.post(url)
        self.assertTemplateUsed(response, 'akanda/alias/networks/create.html')

    def test_create_network_alias_message(self):
        url = reverse('horizon:nova:networking:alias:networks:create')
        response = self.client.post(url, self.form_data)
        storage = default_storage(response.request)
        message_cookie = response.cookies['messages'].value
        messages = [m.message for m in storage._decode(message_cookie)]
        msg = "Successfully created network alias: %s"
        self.assertIn(msg % self.form_data['name'], messages)
        self.assertMessageCount(success=1)

    @patch('alias.views.networks.quantum_extensions_client.networkalias_get')
    def test_update_network_alias(self, get_obj):
        url = reverse(
            'horizon:nova:networking:alias:networks:edit', args=['1'])
        network_ref = {'name': 'net1', 'cidr': '192.168.1.1',
                       'groups': 1, 'id': 1}
        get_obj.return_value = network_ref
        response = self.client.post(url)
        self.assertItemsEqual(
            response.context['network_alias'], network_ref)

    @patch('alias.views.networks.quantum_extensions_client.networkalias_get')
    def test_update_network_alias_assert_template(self, get_obj):
        url = reverse(
            'horizon:nova:networking:alias:networks:edit', args=['1'])
        network_ref = {'name': 'net1', 'cidr': '192.168.1.1',
                       'groups': 1, 'id': 1}
        get_obj.return_value = network_ref
        response = self.client.post(url)
        self.assertTemplateUsed(
            response, 'akanda/alias/networks/edit_rules.html')

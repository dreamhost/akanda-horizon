from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from horizon import forms
from horizon import messages
from horizon import exceptions

from akanda.horizon.api import quantum_extensions_client
from akanda.horizon import common
from akanda.horizon.tabs import firewall_tab_redirect


def get_port_aliases(request):
    port_aliases = [(port.id, port.alias_name) for port in
                    quantum_extensions_client.portalias_list(request)]
    port_aliases.insert(0, ('Custom', 'Custom'))
    port_aliases.insert(0, ('', ''))
    return port_aliases


def get_networks_aliases(request):
    return [(network.id, network.alias_name) for network in
            quantum_extensions_client.networkalias_list(request)]


class BaseFirewallRuleForm(forms.SelfHandlingForm):
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    source_network_alias = forms.ChoiceField(
        label=_("Network Alias"), choices=())
    source_port_alias = forms.ChoiceField(
        label=_("Port Alias"), choices=())
    source_protocol = forms.ChoiceField(
        label=_("Protocol"), choices=common.NEW_PROTOCOL_CHOICES,
        required=False)
    source_public_port = forms.CharField(
        label=_("Public Port"), required=False)

    destination_network_alias = forms.ChoiceField(
        label=_("Network Alias"), choices=())
    destination_port_alias = forms.ChoiceField(
        label=_("Port Alias"), choices=())
    destination_protocol = forms.ChoiceField(
        label=_("Protocol"), choices=common.NEW_PROTOCOL_CHOICES,
        required=False)
    destination_public_port = forms.CharField(
        label=_("Public Port"), required=False)

    policy = forms.ChoiceField(
        label=_("Policy"), choices=common.POLICY_CHOICES)

    def __init__(self, *args, **kwargs):
        super(BaseFirewallRuleForm, self).__init__(*args, **kwargs)
        port_alias_choices = get_port_aliases(self.request)
        self.fields['source_port_alias'] = forms.ChoiceField(
            choices=port_alias_choices)
        self.fields['destination_port_alias'] = forms.ChoiceField(
            choices=port_alias_choices)
        network_alias_choices = get_networks_aliases(self.request)
        self.fields['source_network_alias'] = forms.ChoiceField(
            choices=network_alias_choices)
        self.fields['destination_network_alias'] = forms.ChoiceField(
            choices=network_alias_choices)


class CreateFirewallRuleForm(BaseFirewallRuleForm):
    def handle(self, request, data):
        try:
            result = self._create_firewall_rule(request, data)
            messages.success(request, _('Successfully created firewall rule'))
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"),
                firewall_tab_redirect())
            exceptions.handle(request, _('Unable to create firewall rule.'),
                              redirect=redirect)

    def _create_firewall_rule(self, request, data):
        # from akanda.horizon.fakes import FirewallRuleManager
        # from akanda.horizon.fakes import PortAliasManager
        # if data['source_port_alias'] != 'Custom':
        #     source_port_alias = PortAliasManager.get(
        #         request, data['source_port_alias'])
        #     data['source_protocol'] = source_port_alias._protocol
        #     data['source_public_port'] = source_port_alias._ports

        # if data['destination_port_alias'] != 'Custom':
        #     destination_port_alias = PortAliasManager.get(
        #         request, data['destination_port_alias'])
        #     data['destination_protocol'] = destination_port_alias._protocol
        #     data['destination_public_port'] = destination_port_alias._ports

        # FirewallRuleManager.create(request, data)
        return quantum_extensions_client.filterrule_create(request, data)


class EditFirewallRuleForm(BaseFirewallRuleForm):
    def handle(self, request, data):
        try:
            self._update_firewall_rule(request, data)
            messages.success(request, _('Successfully edited firewall rule'))
            return data
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"),
                firewall_tab_redirect())
            exceptions.handle(request, _('Unable to edit firewall rule.'),
                              redirect=redirect)

    def _update_firewall_rule(self, request, data):
        from akanda.horizon.fakes import FirewallRuleManager
        from akanda.horizon.fakes import PortAliasManager
        if data['source_port_alias'] != 'Custom':
            source_port_alias = PortAliasManager.get(
                request, data['source_port_alias'])
            data['source_protocol'] = source_port_alias._protocol
            data['source_public_port'] = source_port_alias._ports

        if data['destination_port_alias'] != 'Custom':
            destination_port_alias = PortAliasManager.get(
                request, data['destination_port_alias'])
            data['destination_protocol'] = destination_port_alias._protocol
            data['destination_public_port'] = destination_port_alias._ports

        FirewallRuleManager.update(request, data)

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from horizon import forms
from horizon import messages
from horizon import exceptions

from akanda.horizon.api import quantum_extensions_client
from akanda.horizon import common
from akanda.horizon import utils
from akanda.horizon.tabs import firewall_tab_redirect


class BaseFirewallRuleForm(forms.SelfHandlingForm):
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    source_id = forms.ChoiceField(label=_("Address Group"))
    destination_id = forms.ChoiceField(label=_("Network Alias"))
    policy = forms.ChoiceField(label=_("Policy"),
                               choices=common.POLICY_CHOICES,
                               initial='block',)

    def __init__(self, *args, **kwargs):
        super(BaseFirewallRuleForm, self).__init__(*args, **kwargs)
        address_groups_choices = utils.get_address_groups(self.request)
        self.fields['source_id'] = forms.ChoiceField(
            label=_("Address Group"), choices=address_groups_choices)
        self.fields['destination_id'] = forms.ChoiceField(
            label=_("Address Group"), choices=address_groups_choices)


class CreateFirewallRuleForm(BaseFirewallRuleForm):
    source_port_alias = forms.ChoiceField(label=_("Port Alias"), choices=())
    source_protocol = forms.ChoiceField(label=_("Protocol"),
                                        choices=common.NEW_PROTOCOL_CHOICES,
                                        required=False)
    source_public_port = forms.IntegerField(min_value=1,
                                            max_value=65536,
                                            label=_("Public Port"),
                                            required=False)
    destination_port_alias = forms.ChoiceField(label=_("Port Alias"),
                                               choices=())
    destination_protocol = forms.ChoiceField(
        label=_("Protocol"), choices=common.NEW_PROTOCOL_CHOICES,
        required=False)
    destination_public_port = forms.IntegerField(min_value=1,
                                                 max_value=65536,
                                                 label=_("Public Port"),
                                                 required=False)

    def __init__(self, *args, **kwargs):
        super(CreateFirewallRuleForm, self).__init__(*args, **kwargs)
        port_alias_choices = utils.get_port_aliases(self.request)
        self.fields['source_port_alias'] = forms.ChoiceField(
            label=_("Port Alias"), choices=port_alias_choices)
        self.fields['destination_port_alias'] = forms.ChoiceField(
            label=_("Port Alias"), choices=port_alias_choices)

    def clean(self):
        cleaned_data = super(BaseFirewallRuleForm, self).clean()
        s_protocol = None
        d_protocol = None

        msg = u"This field is required."

        if cleaned_data.get('source_port_alias', None):
            if cleaned_data['source_port_alias'] == 'Custom':
                if cleaned_data['source_protocol'] is None:
                    self._errors['source_protocol'] = self.error_class([msg])
                    del cleaned_data["source_protocol"]
                else:
                    s_protocol = cleaned_data['source_protocol']

                if cleaned_data['source_public_port'] is None:
                    self._errors['source_public_port'] = self.error_class(
                        [msg])
                    del cleaned_data["source_public_port"]
            else:
                port_alias = quantum_extensions_client.portalias_get(
                    self.request, cleaned_data['source_port_alias'])
                cleaned_data['source_protocol'] = port_alias['protocol']
                cleaned_data['source_public_port'] = port_alias['port']
                s_protocol = port_alias['protocol']

        if cleaned_data.get('destination_port_alias', None):
            if cleaned_data['destination_port_alias'] == 'Custom':
                if cleaned_data['destination_protocol'] is None:
                    self._errors['destination_protocol'] = self.error_class(
                        [msg])
                    del cleaned_data["destination_protocol"]
                else:
                    d_protocol = cleaned_data["destination_protocol"]

                if cleaned_data['destination_public_port'] is None:
                    self._errors['destination_public_port'] = self.error_class(
                        [msg])
                    del cleaned_data["destination_public_port"]
            else:
                port_alias = quantum_extensions_client.portalias_get(
                    self.request, cleaned_data['destination_port_alias'])
                cleaned_data['destination_protocol'] = port_alias['protocol']
                cleaned_data['destination_public_port'] = port_alias['port']
                d_protocol = port_alias['protocol']

        if s_protocol  and d_protocol:
            if s_protocol != d_protocol:
                raise forms.ValidationError(
                    "The source and destination Port Aliases "
                    "must use the same protocol.")

        return cleaned_data

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
        return quantum_extensions_client.filterrule_create(request, data)


class EditFirewallRuleForm(BaseFirewallRuleForm):
    source_protocol = forms.ChoiceField(label=_("Protocol"),
                                        choices=common.NEW_PROTOCOL_CHOICES)
    source_public_port = forms.IntegerField(min_value=1,
                                            max_value=65536,
                                            label=_("Public Port"))
    destination_protocol = forms.ChoiceField(
        label=_("Protocol"), choices=common.NEW_PROTOCOL_CHOICES)
    destination_public_port = forms.IntegerField(min_value=1,
                                                 max_value=65536,
                                                 label=_("Public Port"))

    def clean(self):
        cleaned_data = super(EditFirewallRuleForm, self).clean()
        source_protocol = cleaned_data.get('source_protocol', None)
        destination_protocol = cleaned_data.get('destination_protocol', None)

        if source_protocol  and destination_protocol:
            if source_protocol != destination_protocol:
                raise forms.ValidationError(
                    "The source and destination Port Aliases "
                    "must use the same protocol.")

        return cleaned_data

    def handle(self, request, data):
        try:
            result = self._update_firewall_rule(request, data)
            messages.success(request, _('Successfully edited firewall rule'))
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"),
                firewall_tab_redirect())
            exceptions.handle(request, _('Unable to edit firewall rule.'),
                              redirect=redirect)

    def _update_firewall_rule(self, request, data):
        return quantum_extensions_client.filterrule_update(request, data)

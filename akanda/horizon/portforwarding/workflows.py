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


from django.utils.translation import ugettext as _

from horizon import workflows
from horizon import forms
from horizon import exceptions
from openstack_dashboard.api.nova import server_list

from akanda.horizon import common
from akanda.horizon import utils
from akanda.horizon.tabs import portforwarding_tab_redirect
from akanda.horizon.api import neutron_extensions_client


def get_instances(request):
    return [(item.id, item.name) for item in server_list(request)[0]]


class DetailsAction(workflows.Action):
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    rule_name = forms.CharField(label=_("Name"), max_length=255)
    instance = forms.ChoiceField(
        label=_("Instance"), choices=())

    class Meta:
        name = _("Details")
        slug = 'details'
        permissions = ()
        help_text = _("You can set up port forwarding rules here by picking "
                      "one of your instances, then which ports you want to "
                      "redirect.")

    def __init__(self, request, context, *args, **kwargs):
        super(DetailsAction, self).__init__(request, context, *args, **kwargs)
        self.fields['instance'] = forms.ChoiceField(
            choices=get_instances(request))


class Details(workflows.Step):
    action_class = DetailsAction
    contributes = ("id", "rule_name", "instance")
    template_name = "akanda/portforwarding/_details_workflow_step.html"


class PortsAction(workflows.Action):
    public_port_alias = forms.ChoiceField(label=_("Port Alias"))
    public_protocol = forms.ChoiceField(label=_("Protocol"),
                                        choices=common.NEW_PROTOCOL_CHOICES,
                                        required=False)
    public_port = forms.IntegerField(label=_("Public Port"),
                                     required=False,
                                     min_value=1,
                                     max_value=65536)

    private_port_alias = forms.ChoiceField(label=_("Port Alias"))
    private_protocol = forms.ChoiceField(label=_("Protocol"),
                                         choices=common.NEW_PROTOCOL_CHOICES,
                                         required=False)
    private_port = forms.IntegerField(label=_("Private Port"),
                                      required=False,
                                      min_value=1,
                                      max_value=65536)

    class Meta:
        name = _("Ports")
        permissions = ()

    def __init__(self, *args, **kwargs):
        super(PortsAction, self).__init__(*args, **kwargs)
        port_alias_choices = utils.get_port_aliases(self.request)
        self.fields['public_port_alias'] = forms.ChoiceField(
            choices=port_alias_choices)
        self.fields['private_port_alias'] = forms.ChoiceField(
            choices=port_alias_choices)

    def clean(self):
        cleaned_data = super(PortsAction, self).clean()
        s_protocol = None
        d_protocol = None

        msg = u"This field is required."

        if cleaned_data.get('public_port_alias', None):
            if cleaned_data['public_port_alias'] == 'Custom':
                if cleaned_data['public_protocol'] is None:
                    self._errors['public_protocol'] = self.error_class([msg])
                    del cleaned_data["public_protocol"]
                else:
                    s_protocol = cleaned_data['public_protocol']

                if cleaned_data['public_port'] is None:
                    self._errors['public_port'] = self.error_class(
                        [msg])
                    del cleaned_data["public_port"]
            else:
                port_alias = neutron_extensions_client.portalias_get(
                    self.request, cleaned_data['public_port_alias'])
                cleaned_data['public_protocol'] = port_alias['protocol']
                cleaned_data['public_port'] = port_alias['port']
                s_protocol = port_alias['protocol']

        if cleaned_data.get('private_port_alias', None):
            if cleaned_data['private_port_alias'] == 'Custom':
                if cleaned_data['private_protocol'] is None:
                    self._errors['private_protocol'] = self.error_class(
                        [msg])
                    del cleaned_data["private_protocol"]
                else:
                    d_protocol = cleaned_data["private_protocol"]

                if cleaned_data['private_port'] is None:
                    self._errors['private_port'] = self.error_class(
                        [msg])
                    del cleaned_data["private_port"]
            else:
                port_alias = neutron_extensions_client.portalias_get(
                    self.request, cleaned_data['private_port_alias'])
                cleaned_data['private_protocol'] = port_alias['protocol']
                cleaned_data['private_port'] = port_alias['port']
                d_protocol = port_alias['protocol']

        if s_protocol and d_protocol:
            if s_protocol != d_protocol:
                raise forms.ValidationError(
                    "The source and destination Port Aliases "
                    "must use the same protocol.")

        return cleaned_data


class Ports(workflows.Step):
    action_class = PortsAction
    depends_on = ("rule_name", "instance")
    contributes = (  # "public_ip",
                     "public_port_alias",
                     "public_protocol",
                     "public_port",
                     # "private_ip",
                     "private_port_alias",
                     "private_protocol",
                     "private_port")
    template_name = "akanda/portforwarding/_form_fields.html"


class PortForwardingRule(workflows.Workflow):
    slug = "create_portforwarding_rule"
    name = _("Create a Rule")
    finalize_button_name = _("Create Rule")
    success_message = _('Port Forwarding Rule successfully created')
    failure_message = _('Unable to create Port Forwarding Rule".')
    success_url = "horizon:project:networking:index"
    default_steps = (Details, Ports)

    def get_success_url(self):
        url = super(PortForwardingRule, self).get_success_url()
        return "%s?tab=%s" % (url, portforwarding_tab_redirect())

    def handle(self, request, data):
        try:
            return self._create_portforwarding_rule(request, data)
        except:
            exceptions.handle(request)
            return False

    def _create_portforwarding_rule(self, request, data):
        return neutron_extensions_client.portforward_create(request, data)


class EditPortsAction(workflows.Action):
    public_protocol = forms.ChoiceField(label=_("Protocol"),
                                        choices=common.NEW_PROTOCOL_CHOICES)
    public_port = forms.IntegerField(label=_("Public Port"),
                                     min_value=1,
                                     max_value=65536)
    private_protocol = forms.ChoiceField(label=_("Protocol"),
                                         choices=common.NEW_PROTOCOL_CHOICES)
    private_port = forms.IntegerField(label=_("Private Port"),
                                      min_value=1,
                                      max_value=65536)

    class Meta:
        name = _("Ports")
        permissions = ()

    def clean(self):
        cleaned_data = super(EditPortsAction, self).clean()
        public_protocol = cleaned_data.get('public_protocol', None)
        private_protocol = cleaned_data.get('private_protocol', None)

        if public_protocol and private_protocol:
            if public_protocol != private_protocol:
                raise forms.ValidationError(
                    "The source and destination Port Aliases "
                    "must use the same protocol.")

        return cleaned_data


class EditPorts(workflows.Step):
    action_class = EditPortsAction
    depends_on = ("rule_name", "instance")
    contributes = ("public_protocol",
                   "public_port",
                   "private_protocol",
                   "private_port")
    template_name = "akanda/portforwarding/_edit_form_fields.html"


class EditPortForwardingRule(workflows.Workflow):
    slug = "edit_portforwarding_rule"
    name = _("Edit a Rule")
    finalize_button_name = _("Edit Rule")
    success_message = _('Port Forwarding Rule successfully edited')
    failure_message = _('Unable to edit Port Forwarding Rule".')
    success_url = "horizon:project:networking:index"
    default_steps = (Details, EditPorts)

    def get_success_url(self):
        url = super(EditPortForwardingRule, self).get_success_url()
        return "%s?tab=%s" % (url, portforwarding_tab_redirect())

    def handle(self, request, data):
        try:
            self._update_portforwarding_rule(request, data)
            return data
        except:
            exceptions.handle(request)
            return False

    def _update_portforwarding_rule(self, request, data):
        return neutron_extensions_client.portforward_update(request, data)

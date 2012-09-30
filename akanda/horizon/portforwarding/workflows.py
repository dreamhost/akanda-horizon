from django.utils.translation import ugettext as _

from horizon import workflows
from horizon import forms
from horizon import exceptions
from horizon.api.nova import server_list

from akanda.horizon import common
from akanda.horizon.tabs import portforwarding_tab_redirect
from akanda.horizon.client import portforward_post

from akanda.horizon.fakes import INSTANCES_FAKE_DATA
from akanda.horizon.fakes import PortAliasManager


def get_port_aliases():
    port_aliases = [(port.id, port.alias_name) for port in
                    PortAliasManager.list_all()]
    port_aliases.insert(0, ('Custom', 'Custom'))
    port_aliases.insert(0, ('', ''))
    return port_aliases


def get_instances(request):
    return server_list(request)


class DetailsAction(workflows.Action):
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    rule_name = forms.CharField(label=_("Name"))
    instance = forms.ChoiceField(
        label=_("Instance"), choices=INSTANCES_FAKE_DATA)

    class Meta:
        name = _("Details")
        slug = 'details'
        permissions = ()
        help_text = _("You can set up port forwarding rules here by picking "
                      "one of your instances, then which ports you want to "
                      "redirect.")


class Details(workflows.Step):
    action_class = DetailsAction
    contributes = ("id", "rule_name", "instance")
    template_name = "akanda/portforwarding/_details_workflow_step.html"


class PortsAction(workflows.Action):
    public_ip = forms.CharField(label=_("Public Ip"), required=False)
    public_port_alias = forms.ChoiceField(label=_("Port Alias"))
    public_protocol = forms.ChoiceField(
        label=_("Protocol"), choices=common.PROTOCOL_CHOICES, required=False)
    public_ports = forms.CharField(label=_("Public Ports"), required=False)
    private_ip = forms.CharField(label=_("Private Ip"), required=False)
    private_port_alias = forms.ChoiceField(label=_("Port Alias"))
    private_protocol = forms.ChoiceField(
        label=_("Protocol"), choices=common.PROTOCOL_CHOICES, required=False)
    private_ports = forms.CharField(label=_("Public Ports"), required=False)

    class Meta:
        name = _("Ports")
        permissions = ()

    def __init__(self, *args, **kwargs):
        super(PortsAction, self).__init__(*args, **kwargs)
        # x = get_instances(self.request)
        port_alias_choices = get_port_aliases()
        self.fields['public_port_alias'] = forms.ChoiceField(
            choices=port_alias_choices)
        self.fields['private_port_alias'] = forms.ChoiceField(
            choices=port_alias_choices)


class Ports(workflows.Step):
    action_class = PortsAction
    depends_on = ("rule_name", "instance")
    contributes = (  # "public_ip",
                     "public_port_alias",
                     "public_protocol",
                     "public_ports",
                     # "private_ip",
                     "private_port_alias",
                     "private_protocol",
                     "private_ports")
    template_name = "akanda/portforwarding/_form_fields.html"


class PortForwardingRule(workflows.Workflow):
    slug = "create_portforwarding_rule"
    name = _("Create a Rule")
    finalize_button_name = _("Create Rule")
    success_message = _('Port Forwarding Rule successfully created')
    failure_message = _('Unable to create Port Forwarding Rule".')
    success_url = "horizon:nova:networking:index"
    default_steps = (Details, Ports)

    def get_success_url(self):
        url = super(PortForwardingRule, self).get_success_url()
        return "%s?tab=%s" % (url, portforwarding_tab_redirect())

    def handle(self, request, data):
        try:
            self._create_portforwarding_rule(request, data)
            return data
        except:
            exceptions.handle(request)
            return False

    def _create_portforwarding_rule(self, request, data):
        # from akanda.horizon.fakes import PortForwardingRuleManager
        from akanda.horizon.fakes import PortAliasManager
        if data['public_port_alias'] != 'Custom':
            public_port_alias = PortAliasManager.get(
                request, data['public_port_alias'])
            data['public_protocol'] = public_port_alias._protocol
            data['public_ports'] = public_port_alias._ports

        if data['private_port_alias'] != 'Custom':
            private_port_alias = PortAliasManager.get(
                request, data['private_port_alias'])
            data['private_protocol'] = private_port_alias._protocol
            data['private_ports'] = private_port_alias._ports

        # data.pop('public_ip')
        # data.pop('private_ip')
        # PortForwardingRuleManager.create(request, data)
        portforward_post(request, data)


class EditPortForwardingRule(workflows.Workflow):
    slug = "edit_portforwarding_rule"
    name = _("Edit a Rule")
    finalize_button_name = _("Edit Rule")
    success_message = _('Port Forwarding Rule successfully edited')
    failure_message = _('Unable to edit Port Forwarding Rule".')
    success_url = "horizon:nova:networking:index"
    default_steps = (Details, Ports)

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
        from akanda.horizon.fakes import PortForwardingRuleManager
        from akanda.horizon.fakes import PortAliasManager

        if data['public_port_alias'] != 'Custom':
            public_port_alias = PortAliasManager.get(
                request, data['public_port_alias'])
            data['public_protocol'] = public_port_alias._protocol
            data['public_ports'] = public_port_alias._ports

        if data['private_port_alias'] != 'Custom':
            private_port_alias = PortAliasManager.get(
                request, data['private_port_alias'])
            data['private_protocol'] = private_port_alias._protocol
            data['private_ports'] = private_port_alias._ports

        PortForwardingRuleManager.update(request, data)

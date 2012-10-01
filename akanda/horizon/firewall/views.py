from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms

from akanda.horizon.tabs import firewall_tab_redirect
from akanda.horizon.firewall.forms import (
    CreateFirewallRuleForm, EditFirewallRuleForm)


class CreateFirewallRuleView(forms.ModalFormView):
    form_class = CreateFirewallRuleForm
    template_name = 'akanda/firewall/create.html'
    success_url = reverse_lazy('horizon:nova:networking:index')

    def get_success_url(self):
        url = super(CreateFirewallRuleView, self).get_success_url()
        return "%s?tab=%s" % (url, firewall_tab_redirect())


class EditFirewallRuleView(forms.ModalFormView):
    form_class = EditFirewallRuleForm
    template_name = 'akanda/firewall/edit.html'
    success_url = reverse_lazy('horizon:nova:networking:index')

    def get_success_url(self):
        url = super(EditFirewallRuleView, self).get_success_url()
        return "%s?tab=%s" % (url, firewall_tab_redirect())

    def _get_object(self, ):
        if not hasattr(self, "_object"):
            try:
                from akanda.horizon.fakes import FirewallRuleManager
                self._object = FirewallRuleManager.get(
                    self.request, self.kwargs['firewall_rule_id'])
            except:
                msg = _('Unable to retrieve firewall rule.')
                redirect = self.get_success_url()
                exceptions.handle(self.request, msg, redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(EditFirewallRuleView, self).get_context_data(**kwargs)
        context['firewall_rule'] = self._get_object()
        return context

    def get_initial(self):
        rule = self._get_object()
        initial_data = {
            'id': self.kwargs['firewall_rule_id'],
            'source_network_alias': rule.source_network_alias,
            'source_port_alias': rule.source_port_alias,
            'destination_network_alias': rule.destination_network_alias,
            'destination_port_alias': rule.destination_port_alias,
            'policy': rule._policy
        }
        if rule.source_port_alias == 'Custom':
            initial_data['source_protocol'] = rule._source_protocol
            initial_data['source_public_port'] = rule.source_public_port

        if rule.destination_port_alias == 'Custom':
            initial_data['destination_protocol'] = rule._destination_protocol
            initial_data['destination_public_port'] = \
                rule.destination_public_port
        return initial_data

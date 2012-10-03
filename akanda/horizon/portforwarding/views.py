from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import workflows

from akanda.horizon.portforwarding.workflows import (
    PortForwardingRule, EditPortForwardingRule)


class CreatePortForwardingRuleView(workflows.WorkflowView):
    workflow_class = PortForwardingRule
    template_name = "nova/instances/launch.html"


class EditPortForwardingRuleView(workflows.WorkflowView):
    workflow_class = EditPortForwardingRule
    template_name = "nova/instances/launch.html"

    def _get_object(self, ):
        if not hasattr(self, "_object"):
            try:
                from akanda.horizon.fakes import PortForwardingRuleManager
                self._object = PortForwardingRuleManager.get(
                    self.request, self.kwargs['portforward_rule_id'])
            except:
                msg = _('Unable to retrieve firewall rule.')
                redirect = self.get_success_url()
                exceptions.handle(self.request, msg, redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(EditPortForwardingRuleView,
                        self).get_context_data(**kwargs)
        context['portforward_rule_id'] = self._get_object()
        return context

    def get_initial(self):
        rule = self._get_object()
        initial_data = {'id': self.kwargs['portforward_rule_id'],
                        'rule_name': rule.rule_name,
                        'instance': rule.instance,
                        'public_port_alias': rule.public_port_alias,
                        'private_port_alias': rule.private_port_alias}

        initial_data['public_protocol'] = ''
        initial_data['public_port'] = ''
        if rule.public_port_alias == 'Custom':
            initial_data['public_protocol'] = rule.public_protocol
            initial_data['public_port'] = rule.public_port

        initial_data['private_protocol'] = ''
        initial_data['private_port'] = ''
        if rule.private_port_alias == 'Custom':
            initial_data['private_protocol'] = rule.private_protocol
            initial_data['private_port'] = rule.private_port
        return initial_data

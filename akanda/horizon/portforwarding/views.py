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

from horizon import exceptions
from horizon import workflows

from akanda.horizon.api import neutron_extensions_client
from akanda.horizon.portforwarding.workflows import (
    PortForwardingRule, EditPortForwardingRule)


class CreatePortForwardingRuleView(workflows.WorkflowView):
    workflow_class = PortForwardingRule


class EditPortForwardingRuleView(workflows.WorkflowView):
    workflow_class = EditPortForwardingRule

    def _get_object(self, ):
        if not hasattr(self, "_object"):
            try:
                self._object = neutron_extensions_client.portforward_get(
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
                        'rule_name': rule['name'],
                        'instance': rule['port']['device_id'],
                        'public_protocol': rule['protocol'],
                        'public_port': rule['public_port'],
                        'private_protocol': rule['protocol'],
                        'private_port': rule['private_port'],
                        }

        return initial_data

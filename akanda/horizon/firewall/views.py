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


from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms

from akanda.horizon.api import neutron_extensions_client
from akanda.horizon.tabs import firewall_tab_redirect
from akanda.horizon.firewall.forms import (
    CreateFirewallRuleForm, EditFirewallRuleForm)


class CreateFirewallRuleView(forms.ModalFormView):
    form_class = CreateFirewallRuleForm
    template_name = 'akanda/firewall/create.html'
    success_url = reverse_lazy('horizon:project:networking:index')

    def get_success_url(self):
        url = super(CreateFirewallRuleView, self).get_success_url()
        return "%s?tab=%s" % (url, firewall_tab_redirect())


class EditFirewallRuleView(forms.ModalFormView):
    form_class = EditFirewallRuleForm
    template_name = 'akanda/firewall/edit.html'
    success_url = reverse_lazy('horizon:project:networking:index')

    def get_success_url(self):
        url = super(EditFirewallRuleView, self).get_success_url()
        return "%s?tab=%s" % (url, firewall_tab_redirect())

    def _get_object(self, ):
        if not hasattr(self, "_object"):
            try:
                self._object = neutron_extensions_client.filterrule_get(
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
        source_id = rule.get('source', {}).get('id', '')
        destination_id = rule.get('destination', {}).get('id', '')
        initial_data = {
            'id': self.kwargs['firewall_rule_id'],
            # 'source_id': rule['source']['id'],
            'source_id': source_id,
            'source_public_port': rule['source_port'],
            'source_protocol': rule['protocol'],
            # 'destination_id': rule['destination']['id'],
            'destination_id': destination_id,
            'destination_public_port': rule['destination_port'],
            'destination_protocol': rule['protocol'],
            'policy': rule['action'],
        }

        return initial_data

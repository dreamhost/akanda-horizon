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

from akanda.horizon.alias.forms import (
    CreateNetworkAliasForm, EditNetworkAliasForm)
from akanda.horizon.api import neutron_extensions_client
from akanda.horizon.tabs import alias_tab_redirect


class CreateNetworkView(forms.ModalFormView):
    form_class = CreateNetworkAliasForm
    template_name = 'akanda/alias/networks/create.html'
    success_url = reverse_lazy('horizon:project:networking:index')

    def get_success_url(self):
        url = super(CreateNetworkView, self).get_success_url()
        return "%s?tab=%s" % (url, alias_tab_redirect())


class EditNetworkAliasView(forms.ModalFormView):
    form_class = EditNetworkAliasForm
    template_name = 'akanda/alias/networks/edit_rules.html'
    success_url = reverse_lazy('horizon:project:networking:index')

    def get_success_url(self):
        url = super(EditNetworkAliasView, self).get_success_url()
        return "%s?tab=%s" % (url, alias_tab_redirect())

    def _get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object = neutron_extensions_client.networkalias_get(
                    self.request, self.kwargs['network_alias_id'])
            except:
                msg = _('Unable to retrieve network alias.')
                redirect = self.get_success_url()
                exceptions.handle(self.request, msg, redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(EditNetworkAliasView, self).get_context_data(**kwargs)
        context['network_alias'] = self._get_object()
        return context

    def get_initial(self):
        network_alias = self._get_object()
        return {'id': self.kwargs['network_alias_id'],
                'name': network_alias['name'],
                'cidr': network_alias['cidr']}

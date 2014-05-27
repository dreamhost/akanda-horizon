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
from django.core.urlresolvers import reverse

from horizon import forms
from horizon import messages
from horizon import exceptions
from horizon.utils import fields

from akanda.horizon.api import neutron_extensions_client
from akanda.horizon.utils import get_address_groups
from akanda.horizon.tabs import alias_tab_redirect


class BaseNetworkAliasForm(forms.SelfHandlingForm):
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    name = forms.CharField(label=_("Name"), max_length=255)
    cidr = fields.IPField(label=_("Network Address"),
                          required=False,
                          initial="",
                          help_text=_("Network address in CIDR format "
                                      "(e.g. 192.168.0.0/24)"),
                          version=fields.IPv4 | fields.IPv6,
                          mask=True)
    group = forms.ChoiceField(label=_("Adddress Group"), choices=())

    def __init__(self, *args, **kwargs):
        super(BaseNetworkAliasForm, self).__init__(*args, **kwargs)
        group = get_address_groups(self.request)
        self.fields['group'] = forms.ChoiceField(choices=group)


class CreateNetworkAliasForm(BaseNetworkAliasForm):
    def handle(self, request, data):
        try:
            result = self._create_network_alias(request, data)
            messages.success(
                request,
                _('Successfully created network alias: %s') % (
                    data['name'],))
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:project:networking:index"),
                alias_tab_redirect())
            exceptions.handle(request, _('Unable to create network alias.'),
                              redirect=redirect)

    def _create_network_alias(self, request, data):
        return neutron_extensions_client.networkalias_create(request, data)


class EditNetworkAliasForm(BaseNetworkAliasForm):
    def handle(self, request, data):
        try:
            result = self._update_network_alias(request, data)
            messages.success(
                request,
                _('Successfully updated '
                  'network alias: %s') % data['name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:project:networking:index"),
                alias_tab_redirect())
            exceptions.handle(request, _('Unable to update network alias.'),
                              redirect=redirect)

    def _update_network_alias(self, request, data):
        return neutron_extensions_client.networkalias_update(request, data)

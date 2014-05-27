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

from akanda.horizon import common
from akanda.horizon.api import neutron_extensions_client
from akanda.horizon.tabs import alias_tab_redirect


class BasePortAliasForm(forms.SelfHandlingForm):
    """
    """
    id = forms.CharField(label=_("Id"),
                         widget=forms.HiddenInput, required=False)
    alias_name = forms.CharField(label=_("Name"), max_length=255)
    protocol = forms.ChoiceField(label=_("Protocol"),
                                 choices=common.NEW_PROTOCOL_CHOICES)
    port = forms.IntegerField(label=_("Port Number"), min_value=0,
                              max_value=65536)


class CreatePortAliasForm(BasePortAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            result = self._create_port_alias(request, data)
            messages.success(
                request,
                _('Successfully created port alias: %s') % data['alias_name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:project:networking:index"),
                alias_tab_redirect())
            exceptions.handle(request, _('Unable to create port alias.'),
                              redirect=redirect)

    def _create_port_alias(self, request, data):
        return neutron_extensions_client.portalias_create(request, data)


class EditPortAliasForm(BasePortAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            result = self._update_port_alias(request, data)
            messages.success(
                request,
                _('Successfully updated port alias: %s') % data['alias_name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:project:networking:index"),
                alias_tab_redirect())
            exceptions.handle(request, _('Unable to edit port alias.'),
                              redirect=redirect)

    def _update_port_alias(self, request, data):
        return neutron_extensions_client.portalias_update(request, data)

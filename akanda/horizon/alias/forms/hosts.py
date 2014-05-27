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


from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from akanda.horizon.api import neutron_extensions_client
from akanda.horizon.tabs import alias_tab_redirect


class BaseHostAliasForm(forms.SelfHandlingForm):
    """
    """
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    name = forms.CharField(label=_("Name"), max_length=255)


class CreateHostAliasForm(BaseHostAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            result = self._create_host_alias(request, data)
            messages.success(
                request,
                _('Successfully created Address Group: %s') % data['name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:project:networking:index"),
                alias_tab_redirect())
            exceptions.handle(request, _('Unable to create Address Group.'),
                              redirect=redirect)

    def _create_host_alias(self, request, data):
        return neutron_extensions_client.addressgroup_create(request, data)


class EditHostAliasForm(BaseHostAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            self._update_host_alias(request, data)
            messages.success(
                request,
                _('Successfully updated Address Group: %s') % data['name'])
            return data
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:project:networking:index"),
                alias_tab_redirect())
            exceptions.handle(request, _('Unable to update Address Group.'),
                              redirect=redirect)

    def _update_host_alias(self, request, data):
        return neutron_extensions_client.addressgroup_update(request, data)

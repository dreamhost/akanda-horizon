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

from horizon import tables

from akanda.horizon.api import neutron_extensions_client


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Firewall Rule")
    data_type_plural = _("Firewall Rules")
    success_url = reverse_lazy('horizon:project:networking:index')

    def get_success_url(self, request=None):
        # import here to avoid circular import
        from akanda.horizon.tabs import firewall_tab_redirect
        url = super(Delete, self).get_success_url(request)
        return "%s?tab=%s" % (url, firewall_tab_redirect())

    def delete(self, request, obj_id):
        neutron_extensions_client.filterrule_delete(request, obj_id)


class Create(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Rule")
    url = "horizon:project:networking:firewall:create"
    classes = ("ajax-modal", "btn-create")


class Edit(tables.LinkAction):
    name = "edit_rule"
    verbose_name = _("Edit Rule")
    url = "horizon:project:networking:firewall:edit"
    classes = ("ajax-modal", "btn-edit")


class FirewallRuleTable(tables.DataTable):
    policy = tables.Column('display_policy', verbose_name=_("Policy"))
    source_ip = tables.Column(
        'display_source_group', verbose_name=_("Source IP"))
    source_ports = tables.Column(
        'display_source_port', verbose_name=_("Source Port"))
    destination_ip = tables.Column(
        'display_destination_group', verbose_name=_("Destionation IP"))
    destination_ports = tables.Column(
        'display_destination_port', verbose_name=_("Destionation Port"))

    class Meta:
        name = "firewall_rule"
        verbose_name = _("Firewall Rules")
        table_actions = (Create, Delete)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return ''

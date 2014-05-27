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
    data_type_singular = _("Port Forward")
    data_type_plural = _("Ports Forward")
    success_url = reverse_lazy('horizon:project:networking:index')

    def get_success_url(self, request=None):
        # import here to avoid circular import
        from akanda.horizon.tabs import portforwarding_tab_redirect
        url = super(Delete, self).get_success_url(request)
        return "%s?tab=%s" % (url, portforwarding_tab_redirect())

    def delete(self, request, obj_id):
        neutron_extensions_client.portforward_delete(request, obj_id)


class Create(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Rule")
    url = "horizon:project:networking:forwarding:create"
    classes = ("ajax-modal", "btn-create")


class Edit(tables.LinkAction):
    name = "edit_rule"
    verbose_name = _("Edit Rule")
    url = "horizon:project:networking:forwarding:edit"
    classes = ("ajax-modal", "btn-edit")


class PortForwardingTable(tables.DataTable):
    rule_name = tables.Column('rule_name', verbose_name=_("Rule Name"))
    instances = tables.Column('display_instance', verbose_name=_("Instance"))
    public_port = tables.Column(
        'display_public_port', verbose_name=_("Public Port"))
    private_port = tables.Column(
        'display_private_port', verbose_name=_("Private Port"))

    class Meta:
        name = "portforwarding"
        verbose_name = _("Port Forwarding")
        table_actions = (Create, Delete,)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return datum.rule_name

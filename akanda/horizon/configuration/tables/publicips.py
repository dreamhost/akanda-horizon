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


import logging

from django import template
from django.utils.translation import ugettext as _

from horizon import tables


LOG = logging.getLogger(__name__)
LOG.debug('importing publicips table')


def get_ips(router):
    template_name = 'akanda/configuration/_router_ips.html'
    context = {'router': router}
    return template.loader.render_to_string(template_name, context)


class PublicIPsTable(tables.DataTable):
    router_name = tables.Column('router_name', verbose_name=_("Router Name"))
    ipaddr = tables.Column(get_ips, verbose_name=_("IP Address"))

    class Meta:
        name = "publicips"
        verbose_name = _("Public IPs")
        table_actions = ()
        row_actions = ()

    def get_object_display(self, datum):
        LOG.debug('get_object_display')
        return 'objdisp'  # datum.router_name

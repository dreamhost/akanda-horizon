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


from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from openstack_dashboard import api


def get_interfaces_data(self):
    try:
        router_id = self.kwargs['router_id']
        router = api.neutron.router_get(self.request, router_id)
        # Filter off the port on the mgt network and router external gateway
        ports = [
            api.neutron.Port(p) for p in router.ports
            if p['device_owner'] not in (
                'network:router_management',
                'network:router_gateway'
            )
        ]
    except Exception:
        ports = []
        msg = _(
            'Port list can not be retrieved for router ID %s' %
            self.kwargs.get('router_id')
        )
        exceptions.handle(self.request, msg)
    for p in ports:
        p.set_id_as_name_if_empty()
    return ports

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


# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2013 NTT MCL Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic import View

from openstack_dashboard import api


class JSONView(View):
    def add_resource_url(self, view, resources):
        tenant_id = self.request.user.tenant_id
        for resource in resources:
            if (resource.get('tenant_id')
                    and tenant_id != resource.get('tenant_id')):
                continue
            resource['url'] = reverse(view, None, [str(resource['id'])])

    def _check_router_external_port(self, ports, router_id, network_id):
        for port in ports:
            if (port['network_id'] == network_id
                    and port['device_id'] == router_id):
                return True
        return False

    def get(self, request, *args, **kwargs):
        data = {}
        # Get nova data
        novaclient = api.nova.novaclient(request)
        servers = novaclient.servers.list()
        data['servers'] = [{'name': server.name,
                            'status': server.status,
                            'id': server.id} for server in servers]
        self.add_resource_url('horizon:project:instances:detail',
                              data['servers'])
        # Get neutron data
        neutronclient = api.neutron.neutronclient(request)
        networks = neutronclient.list_networks()
        subnets = neutronclient.list_subnets()
        ports = neutronclient.list_ports()
        routers = neutronclient.list_routers()
        data['networks'] = sorted(networks.get('networks', []),
                                  key=lambda x: x.get('router:external'),
                                  reverse=True)
        self.add_resource_url('horizon:project:networks:detail',
                              data['networks'])
        data['subnets'] = subnets.get('subnets', [])
        data['ports'] = ports.get('ports', [])
        self.add_resource_url('horizon:project:networks:ports:detail',
                              data['ports'])
        data['routers'] = routers.get('routers', [])
        # user can't see port on external network. so we are
        # adding fake port based on router information
        for router in data['routers']:
            external_gateway_info = router.get('external_gateway_info')
            if not external_gateway_info:
                continue
            external_network = external_gateway_info.get(
                'network_id')
            if not external_network:
                continue
            if self._check_router_external_port(data['ports'],
                                                router['id'],
                                                external_network):
                continue
            fake_port = {'id': 'fake%s' % external_network,
                         'network_id': external_network,
                         'device_id': router['id'],
                         'fixed_ips': []}
            data['ports'].append(fake_port)

        self.add_resource_url('horizon:project:routers:detail',
                              data['routers'])

        # The data model in our custom neutron differ from upstream.
        # In vanilla neutron the dictionary representing a port contains the
        # neutron router id as value of the device_id key but our custom
        # neutron use the akanda vm id. This difference breaks the horizon
        # network topology graph. To fix this problem we take advantage of the
        # fact that the show_router call return a dict with details about all
        # the ports the router is attached to. This allow us to reverse the
        # process and assign to all the port in data['ports'] with
        # device_owner==network:router_interface the correct value for the
        # device_id key

        router_ports = {}
        for router in data['routers']:
            router_details = neutronclient.show_router(router['id'])
            for port in router_details['router'].get('ports', []):
                if port['device_owner'] == 'network:router_interface':
                    router_ports[port['id']] = router['id']

        for port in data['ports']:
            port['device_id'] = router_ports.get(port['id'], port['device_id'])

        json_string = simplejson.dumps(data, ensure_ascii=False)
        return HttpResponse(json_string, mimetype='text/json')

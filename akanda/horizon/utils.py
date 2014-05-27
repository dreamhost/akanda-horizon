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


from akanda.horizon.api import neutron_extensions_client


def get_address_groups(request):
    head = None
    group_list = []
    for group in neutron_extensions_client.addressgroup_list(request):
        if group.name == 'Any':
            head = (group.id, group.name)
        else:
            group_list.append((group.id, group.name))

    if head:
        group_list.insert(0, head)
    return group_list


def get_port_aliases(request):
    any_tcp = None
    any_udp = None
    port_aliases = []
    for port in neutron_extensions_client.portalias_list(request):
        if port.alias_name == 'Any TCP':
            any_tcp = (port.id, port.alias_name)
        elif port.alias_name == 'Any UDP':
            any_udp = (port.id, port.alias_name)
        else:
            port_aliases.append((port.id, port.alias_name))

    if any_tcp:
        port_aliases.append(any_tcp)
    if any_udp:
        port_aliases.append(any_udp)

    port_aliases.append(('Custom', 'Custom'))
    return port_aliases

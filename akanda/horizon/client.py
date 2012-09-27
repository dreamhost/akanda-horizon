# Copyright 2012 New Dream Network, LLC (DreamHost)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# DreamHost Qauntum Extensions
# @author: Murali Raju, New Dream Network, LLC (DreamHost)
# @author: Rosario Disomma, New Dream Network, LLC (DreamHost)

import requests
import json

from horizon.api.nova import server_get

from akanda.horizon.common import PROTOCOL_CHOICES as protocol_choices
PROTOCOL_CHOICES = dict(protocol_choices)


#dhaddresbook
def portforward_get(request):
    headers = {
        "User-Agent": "python-quantumclient",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Auth-Token": request.user.token.id
    }
    r = requests.get('http://0.0.0.0:9696/v2.0/dhportforward.json',
                     headers=headers)
    tmp = r.json.get('portforwards', {})
    portforwards_list = []
    for item in tmp:
        portforward_rule = PortForwardingRule(
            rule_name = item.get('name', 'fake_name'),
            instance = item.get('instance_id', 'instance_id'),
            public_port_alias = item.get('public_port_alias','pub_port_alias'),
            public_protocol = item.get('public_protocol', 0),
            public_ports = item.get('public_port', 'public_port'),
            private_port_alias = item.get('private_port_alias','p_port_alias'),
            private_protocol = item.get('private_protocol',0),
            private_ports = item.get('private_port', 'private_port'),
            id = item.get('id', 'id'),
            request = request
        )
        portforwards_list.append(portforward_rule)
    return portforwards_list


def portforward_post(request, payload):
    headers = {
        "User-Agent": "python-quantumclient",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Auth-Token": request.user.token.id
    }
    
    portforward = {'portforward':{
        'name':  'rule_name',
        'instance_id': '015eff2961d8430ba0c7c483fcb2da7a',
        'protocol': 'tcp',
        'public_port': 333,
        'private_port': 444,
        'op_status': 'ACTIVE',
        'fixed_id': 'fde879e4-07f7-11e2-86a5-080027e60b25'
        }}
    
    r = requests.post('http://0.0.0.0:9696/v2.0/dhportforward.json',
                      headers=headers, data=json.dumps(portforward))
    if r.status_code == requests.codes.created:
        return True
    else:
        return False


class PortForwardingRule(object):
    def __init__(self, rule_name, instance, public_port_alias,
                 public_protocol, public_ports, private_port_alias,
                 private_protocol, private_ports, id=None, request=None):
        self.rule_name = rule_name
        self.instance = instance
        self.public_port_alias = public_port_alias
        self.public_protocol = public_protocol
        self.public_ports = public_ports
        self.private_port_alias = private_port_alias
        self.private_protocol = private_protocol
        self.private_ports = private_ports
        self.id = id
        self.request = request

    @property
    def public_protocol(self, ):
        return self._public_protocol

    @public_protocol.setter
    def public_protocol(self, value):
        if isinstance(value, basestring):
            self._public_protocol = int(value)
        else:
            self._public_protocol = value

    @property
    def public_ports(self):
        return self._public_ports

    @public_ports.setter
    def public_ports(self, value):
        if isinstance(value, basestring):
            self._public_ports = map(int, value.split('-'))
            self._public_ports.sort()
        else:
            self._public_ports = value

    @property
    def private_protocol(self, ):
        return self._private_protocol

    @private_protocol.setter
    def private_protocol(self, value):
        if isinstance(value, basestring):
            self._private_protocol = int(value)
        else:
            self._private_protocol = value

    @property
    def private_ports(self):
        # return self._private_ports
        return self._private_ports

    @private_ports.setter
    def private_ports(self, value):
        if isinstance(value, basestring):
            self._private_ports = map(int, value.split('-'))
            self._private_ports.sort()
        else:
            self._private_ports = value

    @property
    def t_instance(self):
        try:
            instance = server_get(self.request,
                                  self.instance)
            return instance.name
        except:
            return '-'

    @property
    def t_public_ports(self):
        return "%s %s" % (PROTOCOL_CHOICES[self.public_protocol],
                          self.public_ports)

    @property
    def t_private_ports(self):
        return "%s %s" % (PROTOCOL_CHOICES[self.private_protocol],
                          self.private_ports)

    def raw(self):
        data = self.__dict__.copy()
        for k, v in data.items():
            if k.startswith('_'):
                tmp = data.pop(k)
                data[k[1:]] = tmp
        return data


class Network(object):
    def __init__(self, alias_name, cidr, id=None):
        self.alias_name = alias_name
        self.cidr = cidr
        self.id = id or uuid.uuid4().hex

    def raw(self):
        return self.__dict__.copy()

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
# DreamHost Quantum Extensions
# @author: Murali Raju, New Dream Network, LLC (DreamHost)
# @author: Rosario Disomma, New Dream Network, LLC (DreamHost)

import logging

from horizon.api import nova
from horizon.api import quantum
from horizon.api.quantum import quantumclient

from quantumclient.common.exceptions import PortNotFoundClient
from akanda.horizon.common import (
    NEW_PROTOCOL_CHOICES_DICT, POLICY_CHOICES_DICT)


LOG = logging.getLogger(__name__)


def get_protocol(value):
    return NEW_PROTOCOL_CHOICES_DICT[value]


class Port(object):
    def __init__(self, alias_name, protocol, port, id=None):
        self.alias_name = alias_name
        self.protocol = protocol
        self.port = port
        self.id = id

    def display_protocol(self):
        return get_protocol(self.protocol)


class AdressGroup(object):
    def __init__(self, name, id=None):
        self.name = name
        self.id = id


class Network(object):
    def __init__(self, alias_name, cidr, id=None):
        self.alias_name = alias_name
        self.cidr = cidr
        self.id = id


class FilterRule(object):
    def __init__(self, source_network_alias, source_public_port,
                 destination_network_alias, destination_public_port,
                 protocol, policy, request, id=None):
        self.policy = policy
        self.source_network_alias = source_network_alias
        self.source_public_port = source_public_port
        self.destination_network_alias = destination_network_alias
        self.destination_public_port = destination_public_port
        self.protocol = protocol
        self.request = request
        self.id = id

    def display_policy(self):
        return POLICY_CHOICES_DICT[self.policy]

    def display_source_ip(self):
        # network = networkalias_get(self.request, self.source_network_alias)
        # return network.get('cidr')
        return self.source_network_alias

    def display_destination_ip(self):
        # network = networkalias_get(self.request,
        #                            self.destination_network_alias)
        # return network.get('cidr')
        return self.destination_network_alias

    def display_source_port(self):
        return "%s %s" % (get_protocol(self.protocol),
                          self.source_public_port)

    def display_destination_port(self):
        return "%s %s" % (get_protocol(self.protocol),
                          self.destination_public_port)


class PortForwardingRule(object):
    def __init__(self, rule_name, instance_id, public_port,
                 protocol, private_port, request, id=None):
        self.rule_name = rule_name
        self.instance_id = instance_id
        self.public_port = public_port
        self.protocol = protocol
        self.private_port = private_port
        self.request = request
        self.id = id

    def display_public_port(self):
        return "%s %s" % (get_protocol(self.protocol),
                          self.public_port)

    def display_private_port(self):
        return "%s %s" % (get_protocol(self.protocol),
                          self.private_port)

    def display_instance(self):
        try:
            instance = nova.server_get(self.request, self.instance_id)
            return instance.name
        except:
            return '--'


def _mk_url(*args):
    path =  '/'.join(args).lstrip('/')
    if not path.startswith('/'):
        path = '/' + path
    return path


def _list(request, path):
    return quantumclient(request).get(_mk_url(path))


def _get(request, path, obj_id):
    return quantumclient(request).get(_mk_url(path, obj_id))


def _create(request, path, body):
    return quantumclient(request).post(_mk_url(path), body=body)


def _put(request, path, obj_id, body):
    return quantumclient(request).put(_mk_url(path, obj_id), body=body)


def _delete(request, path, obj_id):
    return quantumclient(request).delete(_mk_url(path, obj_id))


def portalias_list(request):
    r = _list(request, 'dhportalias')
    return [Port(item['name'], item['protocol'], item['port'], item['id'])
            for item in r.get('portaliases', {})]


def portalias_get(request, obj_id):
    r = _get(request, 'dhportalias', obj_id)
    return r.get('portalias', {})


def portalias_create(request, body):
    portalias = {'portalias': {
        'name': body['alias_name'],
        'protocol': body['protocol'],
        'port': body['port'],
    }}
    LOG.debug("portalias_create(): body = %s" % body)
    return _create(request, 'dhportalias', portalias)


def portalias_update(request, body):
    obj_id = body.pop('id', '')
    portalias = {'portalias': {
        'name': body['alias_name'],
        'protocol': body['protocol'],
        'port': body['port'],
    }}
    LOG.debug("portalias_update(): body = %s" % body)
    return _put(request, 'dhportalias', obj_id, portalias)


def portalias_delete(request, obj_id):
    return _delete(request, 'dhportalias', obj_id)


def addressbook_list(request):
    r = _list(request, 'dhaddressgroup')
    return [AdressGroup(item['name'], item['id'])
            for item in r.get('addressgroups', {})]


def networkalias_list(request):
    r = _list(request, 'dhaddressentry')
    return [Network(item['name'], item['cidr'], item['id'])
            for item in r.get('addressentries', {})]


def networkalias_get(request, obj_id):
    r = _get(request, 'dhaddressentry', obj_id)
    return r.get('addressentry', {})


def networkalias_create(request, body):
    networkalias = {'addressentry': {
        'name': body['name'],
        'cidr': body['cidr'],
        'group_id': body['group']
    }}
    LOG.debug("networkalias_create(): body = %s" % body)
    return _create(request, 'dhaddressentry', networkalias)


def networkalias_update(request, body):
    obj_id = body.pop('id', '')
    networkalias = {'addressentry': {
        'name': body['name'],
        'cidr': body['cidr'],
    }}
    LOG.debug("networkalias_update(): body = %s" % body)
    return _put(request, 'dhaddressentry', obj_id, networkalias)


def networkalias_delete(request, obj_id):
    return _delete(request, 'dhaddressentry', obj_id)


def filterrule_list(request):
    r = _list(request, 'dhfilterrule')
    return [FilterRule(item.get('source_id', ''), item['source_port'],
                       item.get('destination_id', ''),
                       item['destination_port'],
                       item['protocol'], item['action'], request, item['id'])
            for item in r.get('filterrules', {})]


def filterrule_get(request, obj_id):
    r = _get(request, 'dhfilterrule', obj_id)
    r.raise_for_status(allow_redirects=False)
    return r.json.get('filterrule', {})


def filterrule_create(request, payload):
    filterrule = {'filterrule': {
        'source_alias': payload['source_network_alias'],
        'destination_alias': payload['destination_network_alias'],
        'source_port': payload['source_public_port'],
        'destination_port': payload['destination_public_port'],
        'protocol': payload['source_protocol'],
        'action': payload['policy'],
    }}
    r = _create(request, 'dhfilterrule', filterrule)
    r.raise_for_status(allow_redirects=False)
    return True


def filterrule_update(request, payload):
    obj_id = payload.pop('id', '')
    filterrule = {'filterrule': {
        'source_alias': payload['source_network_alias'],
        'destination_alias': payload['destination_network_alias'],
        'source_port': payload['source_public_port'],
        'destination_port': payload['destination_public_port'],
        'protocol': payload['source_protocol'],
        'action': payload['policy'],
    }}
    r = _put(request, 'dhfilterrule', obj_id, filterrule)
    r.raise_for_status(allow_redirects=False)
    return True


def filterrule_delete(request, obj_id):
    r = _delete(request, 'dhfilterrule', obj_id)
    r.raise_for_status(allow_redirects=False)
    return True


def portforward_list(request):
    r = _list(request, 'dhportforward')
    return [PortForwardingRule(item['name'], '',
                               item['public_port'], item['protocol'],
                               item['private_port'], request, item['id'])
            for item in r.get('portforwards', {})]


def portforward_get(request, obj_id):
    r = _get(request, 'dhportforward', obj_id)
    r.raise_for_status(allow_redirects=False)
    return r.json.get('portforward', {})


def portforward_create(request, payload):
    port_list = quantum.port_list(request)
    try:
        port = port_list[0]
    except IndexError:
        raise PortNotFoundClient

    portforward = {'portforward': {
        'name': payload['rule_name'],
        'instance_id': payload['instance'],
        'protocol': payload['public_protocol'],
        'public_port': payload['public_port'],
        'private_port': payload['private_port'],
        'port_id': port.id
    }}

    r = _create(request, 'dhportforward', portforward)
    r.raise_for_status(allow_redirects=False)
    return True


def portforward_update(request, payload):
    obj_id = payload.pop('id', '')
    portforward = {'portforward': {
        'name': payload['rule_name'],
        'instance_id': payload['instance'],
        'protocol': payload['public_protocol'],
        'public_port': payload['public_port'],
        'private_port': payload['private_port'],
        'port_id': payload['port_id']
    }}
    r = _put(request, 'dhportforward', obj_id, portforward)
    r.raise_for_status(allow_redirects=False)
    return True


def portforward_delete(request, obj_id):
    r = _delete(request, 'dhportforward', obj_id)
    r.raise_for_status(allow_redirects=False)
    return True

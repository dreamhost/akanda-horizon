import uuid

from akanda.horizon.common import PROTOCOL_CHOICES as protocol_choices
from akanda.horizon.common import (POLICY_CHOICES as policy_choices)
from .fake_data import instances_fake_data


PROTOCOL_CHOICES = dict(protocol_choices)
POLICY_CHOICES = dict(policy_choices)


def list_to_string(data):
    return '-'.join(map(str, data))


class Port(object):
    def __init__(self, alias_name, protocol, ports, id=None):
        self.alias_name = alias_name
        self.protocol = protocol
        self.ports = ports
        self.id = id or uuid.uuid4().hex

    @property
    def protocol(self):
        return PROTOCOL_CHOICES[self._protocol]

    @protocol.setter
    def protocol(self, value):
        if isinstance(value, basestring):
            self._protocol = int(value)
        else:
            self._protocol = value

    @property
    def ports(self):
        return '-'.join(map(str, self._ports))

    @ports.setter
    def ports(self, value):
        if isinstance(value, basestring):
            self._ports = map(int, value.split('-'))
            self._ports.sort()
        else:
            self._ports = value

    def raw(self):
        data = self.__dict__.copy()
        for k, v in data.items():
            if k.startswith('_'):
                tmp = data.pop(k)
                data[k[1:]] = tmp
        return data


class Host(object):
    def __init__(self, alias_name, instances, id=None):
        self.alias_name = alias_name
        self._instances = instances
        self.id = id or uuid.uuid4().hex

    @property
    def instances(self):
        instances = [instances_fake_data[instance]['name'] for instance in
                     self._instances]
        instances.sort()
        return ', '.join(instances)

    def raw(self):
        data = self.__dict__.copy()
        for k, v in data.items():
            if k.startswith('_'):
                tmp = data.pop(k)
                data[k[1:]] = tmp
        return data

    def get_instances_list(self):
        return self._instances


class Network(object):
    def __init__(self, alias_name, cidr, id=None):
        self.alias_name = alias_name
        self.cidr = cidr
        self.id = id or uuid.uuid4().hex

    def raw(self):
        return self.__dict__.copy()


class FirewallRule(object):
    """
    """

    def __init__(self, policy, source_network_alias, source_port_alias,
                 source_protocol, source_public_ports,
                 destination_network_alias, destination_port_alias,
                 destination_protocol, destination_public_ports, id=None):
        self.policy = policy
        self.source_network_alias = source_network_alias
        self.source_port_alias = source_port_alias
        self.source_protocol = source_protocol
        self.source_public_ports = source_public_ports
        self.destination_network_alias = destination_network_alias
        self.destination_port_alias = destination_port_alias
        self.destination_protocol = destination_protocol
        self.destination_public_ports = destination_public_ports
        self.id = id or uuid.uuid4().hex

        # avoid circular import
        from akanda.horizon.fakes import NetworkAliasManager
        self.network_manager = NetworkAliasManager

    @property
    def policy(self):
        return POLICY_CHOICES[self._policy]

    @policy.setter
    def policy(self, value):
        if isinstance(value, basestring):
            self._policy = int(value)
        else:
            self._policy = value

    @property
    def source_ip(self):
        network = self.network_manager.get(
            None, self.source_network_alias)
        return network.cidr

    @property
    def destination_ip(self):
        network = self.network_manager.get(
            None, self.destination_network_alias)
        return network.cidr

    @property
    def source_public_ports(self):
        return '-'.join(map(str, self._source_public_ports))

    @source_public_ports.setter
    def source_public_ports(self, value):
        if isinstance(value, basestring):
            self._source_public_ports = map(int, value.split('-'))
            self._source_public_ports.sort()
        else:
            self._source_public_ports = value

    @property
    def source_ports(self):
        return "%s %s" % (self.source_protocol, self.source_public_ports)

    @property
    def source_protocol(self, ):
        return PROTOCOL_CHOICES[self._source_protocol]

    @source_protocol.setter
    def source_protocol(self, value):
        if isinstance(value, basestring):
            self._source_protocol = int(value)
        else:
            self._source_protocol = value

    @property
    def destination_public_ports(self):
        return '-'.join(map(str, self._destination_public_ports))

    @destination_public_ports.setter
    def destination_public_ports(self, value):
        if isinstance(value, basestring):
            self._destination_public_ports = map(int, value.split('-'))
            self._destination_public_ports.sort()
        else:
            self._destination_public_ports = value

    @property
    def destination_ports(self):
        return "%s %s" % (self.destination_protocol,
                          self.destination_public_ports)

    @property
    def destination_protocol(self):
        return PROTOCOL_CHOICES[self._destination_protocol]

    @destination_protocol.setter
    def destination_protocol(self, value):
        if isinstance(value, basestring):
            self._destination_protocol = int(value)
        else:
            self._destination_protocol = value

    def raw(self):
        data = self.__dict__.copy()
        for k, v in data.items():
            if k.startswith('_'):
                tmp = data.pop(k)
                data[k[1:]] = tmp
        data.pop('network_manager')
        return data


class PortForwardingRule(object):
    def __init__(self, rule_name, instance, public_port_alias,
                 public_protocol, public_ports, private_port_alias,
                 private_protocol, private_ports, id=None):
        self.rule_name = rule_name
        self.instance = instance
        self.public_port_alias = public_port_alias
        self.public_protocol = public_protocol
        self.public_ports = public_ports
        self.private_port_alias = private_port_alias
        self.private_protocol = private_protocol
        self.private_ports = private_ports
        self.id = id or uuid.uuid4().hex

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
        # return self._public_ports
        return '-'.join(map(str, self._public_ports))

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
        return '-'.join(map(str, self._private_ports))

    @private_ports.setter
    def private_ports(self, value):
        if isinstance(value, basestring):
            self._private_ports = map(int, value.split('-'))
            self._private_ports.sort()
        else:
            self._private_ports = value

    @property
    def t_instance(self):
        return instances_fake_data[self.instance]['name']

    @property
    def t_public_ports(self):
        # return "%s %s" % (PROTOCOL_CHOICES[self.public_protocol],
        #                   list_to_string(self.public_ports))
        return "%s %s" % (PROTOCOL_CHOICES[self.public_protocol],
                          self.public_ports)

    @property
    def t_private_ports(self):
        # return "%s %s" % (PROTOCOL_CHOICES[self.private_protocol],
        #                   list_to_string(self.private_ports))
        return "%s %s" % (PROTOCOL_CHOICES[self.private_protocol],
                          self.private_ports)

    def raw(self):
        data = self.__dict__.copy()
        for k, v in data.items():
            if k.startswith('_'):
                tmp = data.pop(k)
                data[k[1:]] = tmp
        return data

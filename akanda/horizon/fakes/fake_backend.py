import requests

from .fake_models import (
    Port, Host, Network, FirewallRule, PortForwardingRule)


class DictKvs(dict):
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def set(self, key, value):
        if isinstance(value, dict):
            self[key] = value.copy()
        else:
            self[key] = value[:]

    def delete(self, key):
        del self[key]


class Manager(object):
    def __init__(self, db):
        self.db = db

    def delete(self, request, obj_id):
        del self.db[obj_id]

    def get(self, request, obj_id):
        return obj_id


class PortAliasManager(Manager):
    def list_all(self, request=None):
        #return [Port(**v) for v in self.db.values()]
        r = requests.get("http://0.0.0.0:9696/v2/extensions")

    def get(self, request, obj_id):
        # user = request.user
        # tenant_id = request.user.tenant_id
        return Port(**self.db[obj_id])

    def create(self, request, obj):
        obj = Port(**obj)
        self.db[obj.id] = obj.raw()

    def update(self, request, obj):
        obj = Port(**obj)
        self.db[obj.id] = obj.raw()


class HostAliasManager(Manager):
    def list_all(self, request=None):
        return [Host(**v) for v in self.db.values()]

    def get(self, request, obj_id):
        return Host(**self.db[obj_id])

    def create(self, request, obj):
        obj = Host(**obj)
        self.db[obj.id] = obj.raw()

    def update(self, request, obj):
        obj = Host(**obj)
        self.db[obj.id] = obj.raw()


class NetworkAliasManager(Manager):
    def list_all(self, request=None):
        return [Network(**v) for v in self.db.values()]

    def get(self, request, obj_id):
        return Network(**self.db[obj_id])

    def create(self, request, obj):
        obj = Network(**obj)
        self.db[obj.id] = obj.raw()

    def update(self, request, obj):
        obj = Network(**obj)
        self.db[obj.id] = obj.raw()


class FirewallRuleManager(Manager):
    def list_all(self, request=None):
        return [FirewallRule(**v) for v in self.db.values()]

    def create(self, request, obj):
        obj = FirewallRule(**obj)
        self.db[obj.id] = obj.raw()

    def get(self, request, obj_id):
        return FirewallRule(**self.db[obj_id])

    def update(self, request, obj):
        obj = FirewallRule(**obj)
        self.db[obj.id] = obj.raw()


class PortForwardingRuleManager(Manager):
    def list_all(self, request=None):
        return [PortForwardingRule(**v) for v in self.db.values()]

    def create(self, request, obj):
        obj = PortForwardingRule(**obj)
        self.db[obj.id] = obj.raw()

    def get(self, request, obj_id):
        return PortForwardingRule(**self.db[obj_id])

    def update(self, request, obj):
        obj = PortForwardingRule(**obj)
        self.db[obj.id] = obj.raw()

import fake_backend
import fake_data


INSTANCES = [(k, v['name']) for k, v in
             fake_data.instances_fake_data.items()]
INSTANCES_FAKE_DATA = sorted(INSTANCES, key=lambda instance: instance[1])

PORT_ALIASES_DB = fake_backend.DictKvs(fake_data.port_aliases_fake_data)
PortAliasManager = fake_backend.PortAliasManager(PORT_ALIASES_DB)

HOST_ALIAS_DB = fake_backend.DictKvs(fake_data.host_aliases_fake_data)
HostAliasManager = fake_backend.HostAliasManager(HOST_ALIAS_DB)

NETWORK_ALIASES_DB = fake_backend.DictKvs(fake_data.network_aliases_fake_data)
NetworkAliasManager = fake_backend.NetworkAliasManager(NETWORK_ALIASES_DB)

FIREWALL_RULES_DB = fake_backend.DictKvs(fake_data.firewall_rules_fake_data)
FirewallRuleManager = fake_backend.FirewallRuleManager(FIREWALL_RULES_DB)

PORTFORWARDING_RULE_DB = fake_backend.DictKvs(
    fake_data.portforwarding_rules_fake_data)
PortForwardingRuleManager = fake_backend.PortForwardingRuleManager(
    PORTFORWARDING_RULE_DB)

from akanda.horizon.api import quantum_extensions_client


def get_address_groups(request):
    head = None
    group_list = []
    for group in quantum_extensions_client.addressgroup_list(request):
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
    for port in quantum_extensions_client.portalias_list(request):
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

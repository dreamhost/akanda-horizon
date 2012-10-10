from akanda.horizon.api import quantum_extensions_client


def get_address_groups(request):
    return [(group.id, group.name)
            for group in quantum_extensions_client.addressgroup_list(request)]

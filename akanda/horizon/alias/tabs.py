from django.utils.translation import ugettext as _

from horizon import tabs

from .tables import PortAliasTable, HostAliasTable, NetworkAliasTable


class AliasTab(tabs.TableTab):
    name = _("Alias")
    slug = "alias_tab"
    table_classes = (PortAliasTable, HostAliasTable, NetworkAliasTable)
    template_name = "akanda/alias/index.html"
    # preload = False

    def get_ports_data(self):
        from akanda.horizon.fakes import PortAliasManager
        return PortAliasManager.list_all(self.request)

    def get_hosts_data(self):
        from akanda.horizon.fakes import HostAliasManager
        return HostAliasManager.list_all(self.request)

    def get_networks_data(self):
        from akanda.horizon.fakes import NetworkAliasManager
        networks = NetworkAliasManager.list_all(self.request)
        return sorted(networks, key=lambda network: network.alias_name)

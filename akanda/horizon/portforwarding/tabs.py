from django.utils.translation import ugettext as _

from horizon import tabs

from akanda.horizon import client
from akanda.horizon.portforwarding.tables import PortForwardingTable


class PortForwardingTab(tabs.TableTab):
    name = _("Port Forwarding")
    slug = "portforwarding"
    table_classes = (PortForwardingTable,)
    template_name = "horizon/common/_detail_table.html"

    def get_portforwarding_data(self):
        return client.portforward_list(self.request)

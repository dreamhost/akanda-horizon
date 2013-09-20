from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from openstack_dashboard import api


def get_interfaces_data(self):
    try:
        router_id = self.kwargs['router_id']
        ports = api.quantum.port_list(self.request,
                                      router_id=router_id)
    except Exception:
        ports = []
        msg = _('Port list can not be retrieved.')
        exceptions.handle(self.request, msg)
    for p in ports:
        p.set_id_as_name_if_empty()
    return ports

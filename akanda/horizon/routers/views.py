from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from openstack_dashboard import api


def get_interfaces_data(self):
    try:
        router_id = self.kwargs['router_id']
        router = api.quantum.router_get(self.request, router_id)
        # Note(rods): Right now we are listing, for both normal and
        #             admin users, all the ports on the user's networks
        #             the router is associated with. We may want in the
        #             future show the ports on the mgt and the external
        #             networks for the admin users.
        ports = [api.quantum.Port(p) for p in router.ports
                 if p['device_owner'] == 'network:router_interface']
    except Exception:
        ports = []
        msg = _(
            'Port list can not be retrieved for router ID %s' %
            self.kwargs.get('router_id')
        )
        exceptions.handle(self.request, msg)
    for p in ports:
        p.set_id_as_name_if_empty()
    return ports

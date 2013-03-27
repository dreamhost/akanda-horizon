from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.project.dashboard import Project


class AkandaNetworking(horizon.Panel):
    name = _("Akanda Networking")
    slug = "networking"


Project.register(AkandaNetworking)

from django.utils.translation import ugettext_lazy as _

import horizon

from horizon.dashboards.nova.dashboard import Nova


class AkandaNetworking(horizon.Panel):
    name = _("Akanda Networking")
    slug = "networking"


Nova.register(AkandaNetworking)

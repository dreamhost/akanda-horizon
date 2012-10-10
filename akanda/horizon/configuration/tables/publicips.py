
import logging

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import tables


LOG = logging.getLogger(__name__)
LOG.debug('importing publicips table')


class PublicIPsTable(tables.DataTable):
    router_name = tables.Column('router_name', verbose_name=_("Router Name"))
    ipaddr = tables.Column('ipaddr', verbose_name=_("IP Address"))

    class Meta:
        name = "publicips"
        verbose_name = _("Public IPs")
        table_actions = ()
        row_actions = ()

    def get_object_display(self, datum):
        LOG.debug('get_object_display')
        return 'objdisp'  #datum.router_name

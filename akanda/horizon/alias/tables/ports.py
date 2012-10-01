from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import tables

from akanda.horizon import client


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Port Alias")
    data_type_plural = _("Port Aliases")
    success_url = reverse_lazy('horizon:nova:networking:index')

    def delete(self, request, obj_id):
        client.portalias_delete(request, obj_id)


class Create(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Alias")
    url = "horizon:nova:networking:alias:ports:create"
    classes = ("ajax-modal", "btn-create")


class Edit(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Alias")
    url = "horizon:nova:networking:alias:ports:edit"
    classes = ("ajax-modal", "btn-edit")


class PortAliasTable(tables.DataTable):
    alias_name = tables.Column('alias_name', verbose_name=_("Alias Name"))
    protocol = tables.Column('display_protocol', verbose_name=_("Protocol"))
    ports = tables.Column('port', verbose_name=_("Port"))

    class Meta:
        name = "ports"
        verbose_name = _("Port Aliases")
        table_actions = (Create, Delete)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return datum.alias_name

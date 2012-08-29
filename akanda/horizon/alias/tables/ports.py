from django.utils.translation import ugettext as _

from horizon import tables


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Port Alias")
    data_type_plural = _("Port Aliases")

    def delete(self, request, obj_id):
        from akanda.horizon.fakes import PortAliasManager
        PortAliasManager.delete(request, obj_id)


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
    protocol = tables.Column('protocol', verbose_name=_("Protocol"))
    ports = tables.Column('ports', verbose_name=_("Ports"))

    class Meta:
        name = "ports"
        verbose_name = _("Port Aliases")
        table_actions = (Create, Delete)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return datum.alias_name

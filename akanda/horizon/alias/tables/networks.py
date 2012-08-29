from django.utils.translation import ugettext as _

from horizon import tables


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Network")
    data_type_plural = _("Networks")

    def delete(self, request, obj_id):
        from akanda.horizon.fakes import NetworkAliasManager
        NetworkAliasManager.delete(request, obj_id)


class Create(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Alias")
    url = "horizon:nova:networking:alias:networks:create"
    classes = ("ajax-modal", "btn-create")


class Edit(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Alias")
    url = "horizon:nova:networking:alias:networks:edit"
    classes = ("ajax-modal", "btn-edit")


class NetworkAliasTable(tables.DataTable):
    alias_name = tables.Column('alias_name', verbose_name=_("Alias Name"))
    cidr = tables.Column('cidr', verbose_name=_("CIDR"))

    class Meta:
        name = "networks"
        verbose_name = _("Network Aliases")
        table_actions = (Create, Delete,)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return datum.alias_name

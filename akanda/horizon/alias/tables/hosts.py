from django.utils.translation import ugettext as _

from horizon import tables


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Host")
    data_type_plural = _("Hosts")

    def delete(self, request, obj_id):
        from akanda.horizon.fakes import HostAliasManager
        HostAliasManager.delete(request, obj_id)


class Create(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Alias")
    url = "horizon:nova:networking:alias:hosts:create"
    classes = ("ajax-modal", "btn-create")


class Edit(tables.LinkAction):
    name = "edit_host"
    verbose_name = _("Edit Alias")
    url = "horizon:nova:networking:alias:hosts:edit"
    classes = ("ajax-modal", "btn-edit")


class HostAliasTable(tables.DataTable):
    alias_name = tables.Column('alias_name', verbose_name=_("Alias Name"))
    instances = tables.Column('instances', verbose_name=_("Instances"))

    class Meta:
        name = "hosts"
        verbose_name = _("Host Aliases")
        table_actions = (Create, Delete,)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return datum.alias_name

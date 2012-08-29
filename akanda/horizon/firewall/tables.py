from django.utils.translation import ugettext as _

from horizon import tables


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Firewall Rule")
    data_type_plural = _("Firewall Rules")

    def delete(self, request, obj_id):
        from akanda.horizon.fakes import FirewallRuleManager
        FirewallRuleManager.delete(request, obj_id)


class Create(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Rule")
    url = "horizon:nova:networking:firewall:create"
    classes = ("ajax-modal", "btn-create")


class Edit(tables.LinkAction):
    name = "edit_rule"
    verbose_name = _("Edit Rule")
    url = "horizon:nova:networking:firewall:edit"
    classes = ("ajax-modal", "btn-edit")


class FirewallRuleTable(tables.DataTable):
    policy = tables.Column('policy', verbose_name=_("Policy"))
    source_ip = tables.Column(
        'source_ip', verbose_name=_("Source IP"))
    source_ports = tables.Column(
        'source_ports', verbose_name=_("Source Ports"))
    destination_ip = tables.Column(
        'destination_ip', verbose_name=_("Destionation IP"))
    destination_ports = tables.Column(
        'destination_ports', verbose_name=_("Destionation Ports"))

    class Meta:
        name = "firewall_rule"
        verbose_name = _("Firewall Rules")
        table_actions = (Create, Delete)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return ''

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import tables


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Port Forward")
    data_type_plural = _("Ports Forward")
    success_url = reverse_lazy('horizon:nova:networking:index')

    def get_success_url(self, request=None):
        # import here to avoid circular import
        from akanda.horizon.tabs import portforwarding_tab_redirect
        url = super(Delete, self).get_success_url(request)
        return "%s?tab=%s" % (url, portforwarding_tab_redirect())

    def delete(self, request, obj_id):
        from akanda.horizon.fakes import PortForwardingRuleManager
        PortForwardingRuleManager.delete(request, obj_id)


class Create(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Rule")
    url = "horizon:nova:networking:forwarding:create"
    classes = ("ajax-modal", "btn-create")


class Edit(tables.LinkAction):
    name = "edit_rule"
    verbose_name = _("Edit Rule")
    url = "horizon:nova:networking:forwarding:edit"
    classes = ("ajax-modal", "btn-edit")


class PortForwardingTable(tables.DataTable):
    rule_name = tables.Column('rule_name', verbose_name=_("Rule Name"))
    instances = tables.Column('t_instance', verbose_name=_("Instance"))
    public_ports = tables.Column(
        't_public_ports', verbose_name=_("Public Ports"))
    private_ports = tables.Column(
        't_private_ports', verbose_name=_("Private Ports"))

    class Meta:
        name = "portforwarding"
        verbose_name = _("Port Forwarding")
        table_actions = (Create, Delete,)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return datum.rule_name

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import tables


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Firewall Rule")
    data_type_plural = _("Firewall Rules")
    success_url = reverse_lazy('horizon:nova:networking:index')

    def get_success_url(self, request=None):
        # import here to avoid circular import
        from akanda.horizon.tabs import firewall_tab_redirect
        url = super(Delete, self).get_success_url(request)
        return "%s?tab=%s" % (url, firewall_tab_redirect())

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

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from horizon import forms
from horizon import messages
from horizon import exceptions

from akanda.horizon import common
from akanda.horizon.tabs import alias_tab_redirect
from akanda.horizon.client import portalias_create


class BasePortAliasForm(forms.SelfHandlingForm):
    """
    """
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    alias_name = forms.CharField(label=_("Name"),)
    protocol = forms.ChoiceField(
        label=_("Protocol"), choices=common.NEW_PROTOCOL_CHOICES)
    port = forms.IntegerField(label=_("Port Number"))


class CreatePortAliasForm(BasePortAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            result = self._create_port_alias(request, data)
            messages.success(
                request,
                _('Successfully created port alias: %s') % data['alias_name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to create port alias.'),
                              redirect=redirect)

    def _create_port_alias(self, request, data):
        return portalias_create(request, data)


class EditPortAliasForm(BasePortAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            self._update_port_alias(request, data)
            messages.success(
                request,
                _('Successfully updated port alias: %s') % data['alias_name'])
            return data
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to create port alias.'),
                              redirect=redirect)

    def _update_port_alias(self, request, data):
        from akanda.horizon.fakes import PortAliasManager
        PortAliasManager.update(request, data)

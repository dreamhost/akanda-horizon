from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from horizon import forms
from horizon import messages
from horizon import exceptions

from akanda.horizon import client
from akanda.horizon.tabs import alias_tab_redirect


class BaseNetworkAliasForm(forms.SelfHandlingForm):
    """
    """
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    alias_name = forms.CharField(label=_("Name"),)
    cidr = forms.GenericIPAddressField(label=_("CIDR"))


class CreateNetworkAliasForm(BaseNetworkAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            result = self._create_network_alias(request, data)
            messages.success(
                request,
                _('Successfully created network alias: %s') % (
                    data['alias_name'],))
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"),
                alias_tab_redirect())
            exceptions.handle(request, _('Unable to create network alias.'),
                              redirect=redirect)

    def _create_network_alias(self, request, data):
        return client.networkalias_create(request, data)


class EditNetworkAliasForm(BaseNetworkAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            self._update_network_alias(request, data)
            messages.success(
                request,
                _('Successfully updated '
                  'network alias: %s') % data['alias_name'])
            return data
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to update network alias.'),
                              redirect=redirect)

    def _update_network_alias(self, request, data):
        from akanda.horizon.fakes import NetworkAliasManager
        NetworkAliasManager.update(self.request, data)

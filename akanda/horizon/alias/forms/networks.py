from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from horizon import forms
from horizon import messages
from horizon import exceptions

from akanda.horizon.api import quantum_extensions_client
from akanda.horizon.tabs import alias_tab_redirect


class BaseNetworkAliasForm(forms.SelfHandlingForm):
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    alias_name = forms.CharField(label=_("Name"), max_length=255)
    cidr = forms.GenericIPAddressField(label=_("CIDR"), unpack_ipv4=True)


class CreateNetworkAliasForm(BaseNetworkAliasForm):
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
        return quantum_extensions_client.networkalias_create(request, data)


class EditNetworkAliasForm(BaseNetworkAliasForm):
    def handle(self, request, data):
        try:
            result = self._update_network_alias(request, data)
            messages.success(
                request,
                _('Successfully updated '
                  'network alias: %s') % data['alias_name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to update network alias.'),
                              redirect=redirect)

    def _update_network_alias(self, request, data):
        return quantum_extensions_client.networkalias_update(request, data)

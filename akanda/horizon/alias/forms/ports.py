from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from horizon import forms
from horizon import messages
from horizon import exceptions

from akanda.horizon import common
from akanda.horizon.api import quantum_extensions_client
from akanda.horizon.tabs import alias_tab_redirect


class BasePortAliasForm(forms.SelfHandlingForm):
    """
    """
    id = forms.CharField(label=_("Id"),
                         widget=forms.HiddenInput, required=False)
    alias_name = forms.CharField(label=_("Name"), max_length=255)
    protocol = forms.ChoiceField(label=_("Protocol"),
                                 choices=common.NEW_PROTOCOL_CHOICES)
    port = forms.IntegerField(label=_("Port Number"), min_value=1,
                              max_value=65536)


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
        return quantum_extensions_client.portalias_create(request, data)


class EditPortAliasForm(BasePortAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            result = self._update_port_alias(request, data)
            messages.success(
                request,
                _('Successfully updated port alias: %s') % data['alias_name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to create port alias.'),
                              redirect=redirect)

    def _update_port_alias(self, request, data):
        return quantum_extensions_client.portalias_update(request, data)

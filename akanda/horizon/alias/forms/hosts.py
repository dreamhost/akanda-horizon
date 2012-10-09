from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from akanda.horizon.api import quantum_extensions_client
from akanda.horizon.tabs import alias_tab_redirect


class BaseHostAliasForm(forms.SelfHandlingForm):
    """
    """
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    name = forms.CharField(label=_("Name"), max_length=255)


class CreateHostAliasForm(BaseHostAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            result = self._create_host_alias(request, data)
            messages.success(
                request,
                _('Successfully created Address Group: %s') % data['name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to create Address Group.'),
                              redirect=redirect)

    def _create_host_alias(self, request, data):
        return quantum_extensions_client.addressgroup_create(request, data)


class EditHostAliasForm(BaseHostAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            self._update_host_alias(request, data)
            messages.success(
                request,
                _('Successfully updated Address Group: %s') % data['name'])
            return data
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to update Address Group.'),
                              redirect=redirect)

    def _update_host_alias(self, request, data):
        return quantum_extensions_client.addressgroup_update(request, data)

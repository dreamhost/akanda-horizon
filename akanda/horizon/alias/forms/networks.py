from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from horizon import forms
from horizon import messages
from horizon import exceptions

from akanda.horizon.api import quantum_extensions_client
from akanda.horizon.tabs import alias_tab_redirect


def get_address_groups(request):
    groups = [(group.id, group.name)
              for group in quantum_extensions_client.addressgroup_list(
                      request)]
    return groups


class BaseNetworkAliasForm(forms.SelfHandlingForm):
    id = forms.CharField(
        label=_("Id"), widget=forms.HiddenInput, required=False)
    name = forms.CharField(label=_("Name"), max_length=255)
    cidr = forms.GenericIPAddressField(label=_("CIDR"), unpack_ipv4=True)
    group = forms.ChoiceField(label=_("Adddress Group"), choices=())

    def __init__(self, *args, **kwargs):
        super(BaseNetworkAliasForm, self).__init__(*args, **kwargs)
        group = get_address_groups(self.request)
        self.fields['group'] = forms.ChoiceField(choices=group)


class CreateNetworkAliasForm(BaseNetworkAliasForm):
    def handle(self, request, data):
        try:
            result = self._create_network_alias(request, data)
            messages.success(
                request,
                _('Successfully created network alias: %s') % (
                    data['name'],))
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
                  'network alias: %s') % data['name'])
            return result
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to update network alias.'),
                              redirect=redirect)

    def _update_network_alias(self, request, data):
        return quantum_extensions_client.networkalias_update(request, data)

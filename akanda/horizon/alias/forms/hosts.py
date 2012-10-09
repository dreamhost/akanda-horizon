from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms
from horizon import messages

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
            self._create_host_alias(request, data)
            messages.success(
                request,
                _('Successfully created host alias: %s') % data['alias_name'])
            return data
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to create host alias.'),
                              redirect=redirect)

    def _create_host_alias(self, request, data):
        from akanda.horizon.fakes import HostAliasManager
        HostAliasManager.create(request, data)


class EditHostAliasForm(BaseHostAliasForm):
    """
    """
    def handle(self, request, data):
        try:
            self._update_host_alias(request, data)
            messages.success(
                request,
                _('Successfully updated host alias: %s') % data['alias_name'])
            return data
        except:
            redirect = "%s?tab=%s" % (
                reverse("horizon:nova:networking:index"), alias_tab_redirect())
            exceptions.handle(request, _('Unable to update host alias.'),
                              redirect=redirect)

    def _update_host_alias(self, request, data):
        from akanda.horizon.fakes import HostAliasManager
        HostAliasManager.update(self.request, data)

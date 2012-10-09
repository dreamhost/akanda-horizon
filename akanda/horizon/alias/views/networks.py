from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms

from akanda.horizon.alias.forms import (
    CreateNetworkAliasForm, EditNetworkAliasForm)
from akanda.horizon.api import quantum_extensions_client
from akanda.horizon.tabs import alias_tab_redirect


class CreateNetworkView(forms.ModalFormView):
    form_class = CreateNetworkAliasForm
    template_name = 'akanda/alias/networks/create.html'
    success_url = reverse_lazy('horizon:nova:networking:index')

    def get_success_url(self):
        url = super(CreateNetworkView, self).get_success_url()
        return "%s?tab=%s" % (url, alias_tab_redirect())


class EditNetworkAliasView(forms.ModalFormView):
    form_class = EditNetworkAliasForm
    template_name = 'akanda/alias/networks/edit_rules.html'
    success_url = reverse_lazy('horizon:nova:networking:index')

    def get_success_url(self):
        url = super(EditNetworkAliasView, self).get_success_url()
        return "%s?tab=%s" % (url, alias_tab_redirect())

    def _get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object = quantum_extensions_client.networkalias_get(
                    self.request, self.kwargs['network_alias_id'])
            except:
                msg = _('Unable to retrieve network alias.')
                redirect = self.get_success_url()
                exceptions.handle(self.request, msg, redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(EditNetworkAliasView, self).get_context_data(**kwargs)
        context['network_alias'] = self._get_object()
        return context

    def get_initial(self):
        network_alias = self._get_object()
        return {'id': self.kwargs['network_alias_id'],
                'name': network_alias['name'],
                'cidr': network_alias['cidr']}

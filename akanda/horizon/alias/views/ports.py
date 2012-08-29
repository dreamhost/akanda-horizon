from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import forms

from akanda.horizon.alias.forms import (
    CreatePortAliasForm, EditPortAliasForm)
from akanda.horizon.tabs import alias_tab_redirect


class CreatePortAliasView(forms.ModalFormView):
    form_class = CreatePortAliasForm
    template_name = 'akanda/alias/ports/create.html'
    success_url = reverse_lazy('horizon:nova:networking:index')

    def get_success_url(self):
        url = super(CreatePortAliasView, self).get_success_url()
        return "%s?tab=%s" % (url, alias_tab_redirect())


class EditPortAliasView(forms.ModalFormView):
    form_class = EditPortAliasForm
    template_name = 'akanda/alias/ports/edit_rules.html'
    success_url = reverse_lazy('horizon:nova:networking:index')

    def get_success_url(self):
        url = super(EditPortAliasView, self).get_success_url()
        return "%s?tab=%s" % (url, alias_tab_redirect())

    def _get_object(self):
        if not hasattr(self, "_object"):
            try:
                from akanda.horizon.fakes import PortAliasManager
                self._object = PortAliasManager.get(
                    self.request, self.kwargs['port_alias_id'])
            except:
                msg = _('Unable to retrieve port alias.')
                redirect = self.get_success_url()
                exceptions.handle(self.request, msg, redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(EditPortAliasView, self).get_context_data(**kwargs)
        context['port_alias'] = self._get_object()
        return context

    def get_initial(self):
        port_alias = self._get_object()
        return {'id': self.kwargs['port_alias_id'],
                'alias_name': port_alias.alias_name,
                'protocol': port_alias.protocol,
                'ports': port_alias.ports}

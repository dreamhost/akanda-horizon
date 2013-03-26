from mock import patch
from django.core.urlresolvers import reverse

from akanda.horizon.tabs import alias_tab_redirect


class AliasFormTest(object):
    """ Base class to test all the forms it the Alias module"""

    @patch('horizon.messages.success')
    def _create_or_update_alias(self, cls, method, msg, msg_attr, success):
        """ Base method used to test what happens after that a form succeed

        to create or edit an alias.

        :cls: form class to test
        :method: method of the cls class to mock
        :msg: message to show
        :msg_attr: form attribute whose value we want to show in the message,
                   like for example the name of the alias
        :success: horizon method used to show the message, it's passed as param
                  by the patch decorator

        """
        with patch.object(cls, method) as mock:
            mock.return_value = True
            form = cls(self.request, data=self.form_data)
            self.assertTrue(form.is_valid())
            self.assertTrue(form.handle(self.request, form.cleaned_data))
            message = "%s: %s"
            success.assert_called_once_with(
                self.request, message % (msg, self.form_data[msg_attr]))

    @patch('horizon.exceptions.handle')
    def _create_or_update_alias_fail(self, cls, method, msg, handle):
        """ Base method used to test all the situation where there is a fail

        after that the form succeed to create or edit an alias.
        :cls: form class to test
        :method: method of the cls class to mock
        :handle: horizon method used to manage the exception raised, it's
                 passed as param by the patch decorator

        """
        form = cls(self.request, data=self.form_data)
        with patch.object(cls, method) as mock:
            mock.return_value = False
            self.assertTrue(form.is_valid())
            self.assertFalse(form.handle(self.request, form.cleaned_data))
            redirect = "%s?tab=%s" % (
                reverse('horizon:project:networking:index'),
                alias_tab_redirect())
            handle.assert_called_once_with(
                self.request, msg, redirect=redirect)

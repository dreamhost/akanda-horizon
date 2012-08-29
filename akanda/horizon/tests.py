# XXX this are disabled until we have a fix for the following warning when
# running the unit tests:
#
#  ImportError: Settings cannot be imported, because environment variable
#  DJANGO_SETTINGS_MODULE is undefined.
#
# Note that the fix should *not* be "set your environment properly" ... unless
# this can be done automatically from the Makefile.
#
#
#from horizon import test
#
#
#class NetworkingTests(test.TestCase):
#    # Unit tests for alias.
#    def test_me(self):
#        self.assertTrue(1 + 1 == 2)

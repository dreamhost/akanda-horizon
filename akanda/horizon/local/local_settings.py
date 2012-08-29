from django.conf import settings


AKANDA_APPS = (
    'akanda.horizon',
)


INSTALLED_APPS = settings.INSTALLED_APPS + AKANDA_APPS

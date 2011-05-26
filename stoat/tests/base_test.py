from django.conf import settings
from django.test import TestCase

class StoatTestCase(TestCase):
    def setUp(self):
        self.OLD_STOAT_TEMPLATES = getattr(settings, 'STOAT_TEMPLATES')
        settings.STOAT_TEMPLATES = {
            'Default': ('stoat/tests/default.html', (
                ('Body',            'text'),
                ('Sidebar Heading', 'char'),
                ('Sidebar Body',    'text'),
            )),
            'Other': ('stoat/tests/other.html', (
                ('Body',            'text'),
                ('Test Int',        'int'),
            )),}

        self.OLD_STOAT_DEFAULT_TEMPLATE = getattr(settings, 'STOAT_DEFAULT_TEMPLATE')
        settings.STOAT_DEFAULT_TEMPLATE = 'Default'

        self.OLD_ROOT_URLCONF = getattr(settings, 'ROOT_URLCONF')
        settings.ROOT_URLCONF = 'stoat.tests.util.urls'

        self.OLD_INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS')
        settings.INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'stoat',)

        self.OLD_MIDDLEWARE_CLASSES = getattr(settings, 'MIDDLEWARE_CLASSES')
        settings.MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'stoat.middleware.StoatMiddleware',)

    def tearDown(self):
        settings.STOAT_TEMPLATES = self.OLD_STOAT_TEMPLATES
        settings.STOAT_DEFAULT_TEMPLATE = self.OLD_STOAT_DEFAULT_TEMPLATE
        settings.ROOT_URLCONF = self.OLD_ROOT_URLCONF
        settings.INSTALLED_APPS = self.OLD_INSTALLED_APPS
        settings.MIDDLEWARE_CLASSES = self.OLD_MIDDLEWARE_CLASSES

def get(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


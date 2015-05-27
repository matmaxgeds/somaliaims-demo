import os

from .settings import *


BOOTSTRAP3 = {
    # The complete URL to the Bootstrap CSS file
    'css_url': '/static/bootstrap/css/bootstrap.min.css',
    'javascript_url': '/static/bootstrap/js/bootstrap.min.js',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ('debug_toolbar', 'django_extensions',)

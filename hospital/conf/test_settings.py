"""
Test settings
- Used to run tests fast on the continuous integration server and locally
"""

import os

# Application
os.environ['APP_NAME'] = os.environ.get('APP_NAME', 'content_first_service')

# Django standard configuration
os.environ['H_DJANGO_SECRET_KEY'] = os.environ.get('H_DJANGO_SECRET_KEY', 'testing_secret')
os.environ['H_DJANGO_ADMIN_URL'] = os.environ.get('H_DJANGO_ADMIN_URL', 'admin')
os.environ['H_VERIFY_SSL'] = os.environ.get('H_VERIFY_SSL', 'false')

# Redis
os.environ['H_REDIS_HOST'] = os.environ.get('H_REDIS_HOST', '127.0.0.1')

# Logging
os.environ['LOGSTASH_HOST'] = os.environ.get('LOGSTASH_HOST', '127.0.0.1')

from hospital.conf.base_settings import *  # noqa: E501,F403  # pylint:disable=wildcard-import,wrong-import-position

# DEBUG
# ------------------------------------------------------------------------------
# Turn debug off so tests run faster
TEMPLATES[0]['OPTIONS']['debug'] = False  # noqa: F405

# PASSWORD HASHING
# ------------------------------------------------------------------------------
# Use fast password hasher so tests run faster
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

if DEBUG:  # noqa: F405
    LOGGING['handlers']['stdout']['filters'].remove('require_debug_true')  # noqa: F405
    LOGGING['handlers']['stdout']['formatter'] = 'testing'  # noqa: F405
    for logger in LOGGING['loggers'].values():  # noqa: F405
        logger['level'] = 'DEBUG'
else:
    LOGGING['handlers']['file']['filters'].remove('require_debug_true')  # noqa: F405
    LOGGING['handlers']['stdout']['formatter'] = 'testing'  # noqa: F405
    for logger in LOGGING['loggers'].values():  # noqa: F405s
        logger['level'] = 'DEBUG'

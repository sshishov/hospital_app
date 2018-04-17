import os

# Application
os.environ['APP_NAME'] = os.environ.get('APP_NAME', 'hospital_app')

# Django standard configuration
os.environ['H_DJANGO_SECRET_KEY'] = os.environ.get('H_DJANGO_SECRET_KEY', 'development_secret')
os.environ['H_DJANGO_ALLOWED_HOSTS'] = os.environ.get('H_DJANGO_ALLOWED_HOSTS', 'localhost, 127.0.0.1')
os.environ['H_DJANGO_ADMIN_URL'] = os.environ.get('H_DJANGO_ADMIN_URL', 'admin/')
os.environ['H_DJANGO_DEBUG'] = os.environ.get('H_DJANGO_DEBUG', 'true')
os.environ['H_VERIFY_SSL'] = os.environ.get('H_VERIFY_SSL', 'false')

# Logging
os.environ['LOGSTASH_HOST'] = os.environ.get('LOGSTASH_HOST', '127.0.0.1')

from hospital.conf.base_settings import *  # noqa: E501,F401,F403  # pylint:disable=wildcard-import,wrong-import-position

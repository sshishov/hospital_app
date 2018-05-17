import os

# Django standard configuration
os.environ['H_DJANGO_ALLOWED_HOSTS'] = os.environ.get('H_DJANGO_ALLOWED_HOSTS', '.1medsys.com')
os.environ['H_DJANGO_ADMIN_URL'] = os.environ.get('H_DJANGO_ADMIN_URL', 'hospital_admin')
os.environ['H_VERIFY_SSL'] = os.environ.get('H_VERIFY_SSL', 'false')

# Redis
os.environ['H_REDIS'] = os.environ.get('H_REDIS', 'redis://redis.1medsys.com:6379/')

# Logging
os.environ['LOGSTASH_HOST'] = os.environ.get('LOGSTASH_HOST', 'logstash.1medsys.com')

from hospital.conf.base_settings import *  # noqa: E501,F403  # pylint:disable=wildcard-import,wrong-import-position

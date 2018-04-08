import os

# Django standard configuration
os.environ['H_DJANGO_ALLOWED_HOSTS'] = os.environ.get('H_DJANGO_ALLOWED_HOSTS', '*')
os.environ['H_DJANGO_ADMIN_URL'] = os.environ.get('H_DJANGO_ADMIN_URL', 'admin')

# Redis
os.environ['H_REDIS'] = os.environ.get(
    'H_REDIS', 'redis://stg-content-first.p4ty9f.0001.euw1.cache.amazonaws.com:6379/',
)

# Logging
os.environ['LOGSTASH_HOST'] = os.environ.get('LOGSTASH_HOST', 'logstash.dubizzlestage.internal')

from hospital.conf.base_settings import *  # noqa: E501,F403  # pylint:disable=wildcard-import,wrong-import-position

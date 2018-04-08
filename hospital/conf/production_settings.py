import os

# Django standard configuration
os.environ['H_DJANGO_ALLOWED_HOSTS'] = os.environ.get('H_DJANGO_ALLOWED_HOSTS', '.dubizzle.com')
os.environ['H_DJANGO_ADMIN_URL'] = os.environ.get('H_DJANGO_ADMIN_URL', 'dubizzle_admin')

# Redis
os.environ['H_REDIS'] = os.environ.get('H_REDIS', 'redis://<redis_url>:6379/')

# Logging
os.environ['LOGSTASH_HOST'] = os.environ.get('LOGSTASH_HOST', 'logman.dubizzlecloud.com')

from hospital.conf.base_settings import *  # noqa: E501,F403  # pylint:disable=wildcard-import,wrong-import-position

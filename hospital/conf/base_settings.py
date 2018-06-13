"""
Django settings for content-first-service project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import itertools
import logging.config
import os
import sys

import dj_database_url

from django.utils.translation import pgettext_lazy

from envparse import Env

#import mongoengine


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Env(
    # Application
    APP_NAME={'cast': str},

    # Django standard configuration
    H_DJANGO_SECRET_KEY={'cast': str},
    H_DJANGO_DEBUG={'cast': bool, 'default': False},
    H_DJANGO_ADMIN_URL={'cast': str},
    H_DJANGO_ALLOWED_HOSTS={'cast': list, 'default': []},
    H_VERIFY_SSL={'cast': bool, 'default': True},

    # Default database
    # H_DB_DEFAULT={'cast': str, 'default': 'mysql://hospital:hospital@127.0.0.1/hospital'},
    H_DB_DEFAULT={'cast': str, 'default': 'djongo://hospital:hospital@127.0.0.1/hospital'},

    # Redis
    H_REDIS={'cast': str, 'default': 'redis://127.0.0.1:6379/'},

    # Logging
    LOG_DIR={'cast': str, 'default': '/var/log/hospital/'},
    LOGSTASH_HOST={'cast': str},
    LOGSTASH_PORT={'cast': int, 'default': 5969},
    LOG_APPNAME={'cast': str, 'default': os.environ['APP_NAME']},
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('H_DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('H_DJANGO_DEBUG')
VERIFY_SSL = env('H_VERIFY_SSL')

ALLOWED_HOSTS = env('H_DJANGO_ALLOWED_HOSTS')

ADMIN_URL = env('H_DJANGO_ADMIN_URL')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap3',
    'jsoneditor',
    'stronghold',

    'hospital',
]

MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'stronghold.middleware.LoginRequiredMiddleware',

    'hospital.middleware.ProjectMiddleware',
]

ROOT_URLCONF = 'hospital.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
            'builtins': [
                'django.contrib.staticfiles.templatetags.staticfiles',
                'django.templatetags.i18n',
                'bootstrap3.templatetags.bootstrap3',
            ],
        },
    },
]

WSGI_APPLICATION = 'hospital.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
dj_database_url.SCHEMES['djongo'] = 'djongo'
DATABASES = {
    'default': {
        key: value for key, value in itertools.chain(
            dj_database_url.parse(env('H_DB_DEFAULT')).items(),
            {'AUTH_SOURCE': 'hospital', 'ENFORCE_SCHEMA': False}.items()
        )
    }
}

# SESSION_ENGINE = 'mongoengine.django.sessions'
#
# _MONGODB_USER = 'hospital'
# _MONGODB_PASSWD = 'hospital'
# _MONGODB_HOST = 'localhost'
# _MONGODB_NAME = 'hospital'
# _MONGODB_DATABASE_HOST = \
#   'mongodb://%s:%s@%s/%s' \
#   % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)
#
# mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)
#
# AUTHENTICATION_BACKENDS = (
#     'mongoengine.django.auth.MongoEngineBackend',
# )

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('ru', pgettext_lazy('language', 'Russian')),
    ('en', pgettext_lazy('language', 'English')),
]

LOCALE_PATHS = (
    os.path.join(os.path.dirname(BASE_DIR), 'locale'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), 'static'),
)
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')

APP_NAME = env('APP_NAME')

# Logstash
LOGSTASH_HOST = env('LOGSTASH_HOST')
LOGSTASH_PORT = env('LOGSTASH_PORT')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'testing': {
            'format': '%(name)s %(levelname)s %(message)s',
        },
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s [%(request_id)s] %(message)s',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{logging_dir}/hospital_app.log'.format(logging_dir=env('LOG_DIR')),
            'formatter': 'default',
            'filters': ['request_id', 'require_debug_true'],
            'maxBytes': 1024 * 1024,
            'backupCount': 3,
        },
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': sys.stdout,
            'filters': ['request_id', 'require_debug_true'],
        },
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': LOGSTASH_HOST,
            'port': LOGSTASH_PORT,
            'filters': ['request_id', 'require_debug_false'],
            'version': 1,
            'fqdn': False,
            'message_type': env('LOG_APPNAME'),
        },
    },
    'loggers': {
        'django.db': {
            'handlers': ['file', 'stdout', 'logstash'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'stdout', 'logstash'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'hospital': {
            'handlers': ['file', 'stdout', 'logstash'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
        'djongo': {
            'handlers': ['file', 'stdout', 'logstash'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
    },
}
logging.config.dictConfig(LOGGING)

# Request ID
LOG_REQUEST_ID_HEADER = 'HTTP_X_CORRELATION_ID'
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = False
REQUEST_ID_RESPONSE_HEADER = LOG_REQUEST_ID_HEADER
LOG_REQUEST_ID_BUS_HEADER = LOG_REQUEST_ID_HEADER[5:].replace('_', '-').upper()

# Auth configuration
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = LOGIN_URL

# Stronghold
STRONGHOLD_PUBLIC_NAMED_URLS = (
    'password_reset',
    'password_reset_done',
)

# django-bootstrap settings
BOOTSTRAP3 = {
    # The URL to the jQuery JavaScript file
    'jquery_url': os.path.join(os.path.dirname(STATIC_URL), 'hospital/vendor/jquery/jquery.min.js'),

    # The Bootstrap base URL
    'base_url': os.path.join(os.path.dirname(STATIC_URL), 'hospital/vendor/bootstrap/'),

    # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
    'include_jquery': True,
}

AUTH_USER_MODEL = 'hospital.User'

# JsonEditor settings
JSON_EDITOR_JS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/4.2.1/jsoneditor.js'
JSON_EDITOR_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/4.2.1/jsoneditor.css'

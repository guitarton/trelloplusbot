"""
Django settings for fa project.

Generated by 'django-admin startproject' using Django 1.8.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import hashlib
import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_cron',
    'bot',
]
try:
    # noinspection PyUnresolvedReferences
    import django_extensions

    INSTALLED_APPS.append('django_extensions')
except ImportError:
    pass

try:
    # noinspection PyUnresolvedReferences
    import debug_toolbar

    INSTALLED_APPS.append('debug_toolbar')
except ImportError:
    pass

BOT_HANDLERS_MODULES = [
    'bot.handlers.private_chat',
    'bot.handlers.group_chat',
    'bot.handlers.admin',
    'bot.handlers.other',
]

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)
# DEBUG_TOOLBAR_PATCH_SETTINGS = False

CRON_CLASSES = [
    'django_cron.cron.FailedRunsNotificationCronJob',
]
DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 31

ROOT_URLCONF = 'trelloplus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                # 'django.template.context_processors.i18n',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(pathname)s:%(lineno)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
        'queries': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'long_queries': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.duration > 0.3 if hasattr(record, 'duration') else True
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'formatter': 'verbose',
        },
        'db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'db.log'),
            'formatter': 'queries',
            'filters': [] if DEBUG else ['long_queries'],
            'maxBytes': 500000,
            'backupCount': 10,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'debug_toolbar': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django_cron': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'TeleBot': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
            'include_html': True,
        },
        'bot.views': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
            'include_html': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null', 'file'],
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['db'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

WSGI_APPLICATION = 'trelloplus.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'trelloplus',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# LOCALE_PATHS = (
#     os.path.join(BASE_DIR, 'locale'),
# )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_URL = '/media/'

MEDIA_DIR = os.path.join('media')
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_DIR)

TELEGRAM_BOT_NAME = ''
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or ''

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
# )

# Logger
ADMINS = ()
MANAGERS = ADMINS

# Testing
TESTING = sys.argv[1:2] in ['test', 'test_coverage']

TG_ADMINS = (
    7975895,  # @ihoru
)

FEEDBACK_GROUP_ID = 0
ERROR_LOG_GROUP_ID = 0

TELEGRAM_RESPONSE_ERROR_ON_EXCEPTION = True  # True - always, False - never

GRAPPELLI_ADMIN_HEADLINE = GRAPPELLI_ADMIN_TITLE = 'Trello Plus Bot'
GRAPPELLI_CLEAN_INPUT_TYPES = False

UNDER_CONSTRUCTION = False

TRELLO_API_KEY = ''
TRELLO_SECRET_KEY = ''

from trelloplus.local_settings import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if DEBUG else logging.ERROR)
handler = logging.FileHandler(os.path.join(BASE_DIR, 'logs', 'debug.log'))
handler.setFormatter(logging.Formatter('%(levelname)s %(asctime)s %(name)s %(pathname)s:%(lineno)d %(message)s'))
handler.setLevel(logging.DEBUG if DEBUG else logging.ERROR)
handler.addFilter(lambda r: not r.name.startswith('requests.') and r.name != 'TeleBot')
handler.addFilter(lambda r: r.name != 'werkzeug')
logger.addHandler(handler)

m = hashlib.md5()
m.update(TELEGRAM_BOT_TOKEN.encode('utf-8'))
TELEGRAM_TOKEN_HASH = m.hexdigest()

# ignore the following error when using ipython:
# /django/db/backends/sqlite3/base.py:57: RuntimeWarning:
# SQLite received a naive datetime (2012-11-02 11:20:15.156506) while time zone support is active.

import warnings

warnings.filterwarnings('ignore', category=RuntimeWarning, module='django.db.backends.sqlite3.base', lineno=57)

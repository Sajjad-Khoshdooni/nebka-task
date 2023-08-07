import os
import sys
from pathlib import Path

import sentry_sdk
from decouple import Csv, config
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool, default=False)
STAGING = config('STAGING', cast=bool, default=False)
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
DEBUG_OR_TESTING = DEBUG or STAGING or TESTING

HOST_URL = config('HOST_URL', default='https://127.0.0.1')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='')
ALLOWED_CIDR_NETS = ['10.0.0.0/16']

CELERY_TASK_ALWAYS_EAGER = config('CELERY_ALWAYS_EAGER', default=False)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',

    'fund'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv(), default='')


ROOT_URLCONF = '_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '_base.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config('DEFAULT_DB_ENGINE', default='django.db.backends.postgresql_psycopg2'),
        'NAME': config('DEFAULT_DB_NAME', default='core_db'),
        'USER': config('DEFAULT_DB_USER', default='postgres'),
        'PASSWORD': config('DEFAULT_DB_PASSWORD', default='postgres'),
        'HOST': config('DEFAULT_DB_HOST', default='localhost'),
        'PORT': config('DEFAULT_DB_PORT', default=5432),
    }
}

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


LANGUAGE_CODE = 'fa-IR'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'public/'))


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ] if DEBUG else [
        'rest_framework.renderers.JSONRenderer',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

sentry_sdk.init(
    dsn=config('SENTRY_DSN', default=''),
    integrations=[
        DjangoIntegration(),
    ],
    environment='staging' if STAGING else 'production',
    traces_sample_rate=0,
    send_default_pii=True
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

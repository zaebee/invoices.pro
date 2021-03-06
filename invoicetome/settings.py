"""
Django settings for invoicetome project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ugettext = lambda s: s

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

sys.path.insert(0, rel('apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!(&sq(&i6a_!&-n$ukc_t-v==d38_s$x$9o1()#=pjzgyez!%z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django_assets',
    'annoying',

    'api',
    'invoice',
    'local',
    'mailer',
    'profiles',

    'registration',
    'widget_tweaks',
    'localeurl',
    'rest_framework',
    'south',
    'json_field',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "local.context_processors.common",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'localeurl.middleware.LocaleURLMiddleware',
)

ROOT_URLCONF = 'invoicetome.urls'

WSGI_APPLICATION = 'invoicetome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'invoices',
        'USER': 'zaebee',
        'PASSWORD': '',
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

EMAIL_BACKEND = "mailer.backend.DbBackend"

TEMPLATE_DIRS = (
    rel('templates'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = (
    ('ru', ugettext('rus')),
    ('en', ugettext('eng')),
)

LOCALE_PATHS = (
    rel('locale'),
)
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = (
    'local.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'ORDERING_PARAM': '-id',
}

ACCOUNT_ACTIVATION_DAYS = 5
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
MEDIA_ROOT = rel('media')
MEDIA_URL = '/media/'

STATIC_ROOT = rel('st')
STATIC_URL = '/st/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    rel('static'),
)

LOCALE_INDEPENDENT_PATHS = (
    r'^/api/',
    r'^/admin/',
    r'^/index',
)

TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/' #use '' for top level template dir, ensure there is a trailing slash
TEMPLATED_EMAIL_FILE_EXTENSION = 'html'

HELLOSIGN_PRESIGN_DIR = rel('hellosign_presign')
HELLOSIGN_SIGNED_DIR = rel('hellosign_signed')

try:
    from settings_local import *
except:
    pass

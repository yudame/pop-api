import logging
import os
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


# DEFINE THE ENVIRONMENT TYPE
PRODUCTION = STAGE = DEMO = LOCAL = False
dt_key = os.environ.get('DEPLOYMENT_TYPE')
if dt_key == 'PRODUCTION':
    PRODUCTION = True
elif dt_key == 'DEMO':
    DEMO = True
elif dt_key == 'STAGE':
    STAGE = True
else:
    LOCAL = True


# Set up logger
if LOCAL:
    log_level = logging.DEBUG
elif PRODUCTION:
    log_level = logging.INFO
else:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = LOCAL or STAGE

WSGI_APPLICATION = 'settings.wsgi.application'

ALLOWED_HOSTS = [
    '.andrello.me',
    '.herokuapp.com',
    'localhost',
]
try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_markup',
]

APPS = [
    'apps.common',
    'apps.communication',
    'apps.user',
    'apps.trello',
    'apps.blog',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(SITE_ROOT, 'templates'), ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.template.context_processors.media',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.static',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}, ]


if PRODUCTION or STAGE:
    DATABASES = {'default': dj_database_url.config()}
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
    ('user', os.path.join(SITE_ROOT, 'apps/user/static')),
    ('blog', os.path.join(SITE_ROOT, 'apps/blog/static')),
)

if LOCAL:
    logger.info("LOCAL environment detected. Importing local_settings.py")
    try:
        from settings.local_settings import *
    except:
        logger.error("Could not successfully import local_settings.py. This is necessary if you are running locally. This file should be in version control.")
        raise

import logging
import os
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
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

INTERNAL_IPS = [
    "127.0.0.1",
]

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
    '.skibi.me',
    '.skibiapp.com',
    '.herokuapp.com',
    'localhost',
]
ROOT_HOSTCONF = 'settings.hosts'
# DEFAULT_HOST = 'skibiapp.com' if not LOCAL else 'localhost'
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
    'django.contrib.humanize',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'storages',
    'debug_toolbar',
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'herokuapp.com',
    'skibi.me',
    'skibiapp.com',
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/trello/setup'
LOGIN_URL = 'admin/login'

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

# Password validation
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
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL = '/static/'
STATIC_ROOT = STATIC_URL = '/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
    # ('user', os.path.join(SITE_ROOT, 'apps/user/static')),
    # ('blog', os.path.join(SITE_ROOT, 'apps/blog/static')),
    # ('trello', os.path.join(SITE_ROOT, 'apps/trello/static')),
)

if LOCAL:
    logger.info("LOCAL environment detected. Importing local_settings.py")
    try:
        from settings.local_settings import *
    except:
        logger.error("Could not successfully import local_settings.py. This is necessary if you are running locally. This file should be in version control.")
        raise


# General apps settings

if PRODUCTION or STAGE:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

logger.info("Importing vendor_services_settings")
try:
    from settings.vendor_services_settings import *
except:
    logger.warning("Failed to import vendor_services_settings.")
    pass

if LOCAL:
    logger.info("LOCAL environment detected. Importing local_settings.py")
    try:
        from settings.local_settings import *
    except:
        logger.error("Could not successfully import local_settings.py. This is necessary if you are running locally. This file should be in version control.")
        raise

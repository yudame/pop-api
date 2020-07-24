from __future__ import absolute_import
import os
import socket
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# DEFINE THE ENVIRONMENT TYPE
PRODUCTION = STAGE = DEMO = LOCAL = False
dt_key = os.environ.get('DEPLOYMENT_TYPE', "LOCAL")
if dt_key == 'PRODUCTION':
    PRODUCTION = True
elif dt_key == 'DEMO':
    DEMO = True
elif dt_key == 'STAGE':
    STAGE = True
else:
    LOCAL = True

DEBUG = LOCAL or STAGE

WSGI_APPLICATION = 'settings.wsgi.application'

ALLOWED_HOSTS = [
    '.yuda.me',
    '.herokuapp.com',
    '.amazonaws.com',
]

if LOCAL:
    INTERNAL_IPS = (
        '127.0.0.1',
        '192.168.*.*',
    )
    ALLOWED_HOSTS += [
        'localhost',
        '127.0.0.1',
        '.ngrok.io',
        '.localhost.run'
    ]
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_WHITELIST = [
        'https://pop-*.herokuapp.com',
        'https://*.yuda.me',
        'https://s3.amazonaws.com',
        # 'http://localhost',
        'http://127.0.0.1',
    ]

if PRODUCTION:
    HOSTNAME, APP_NAME = "pop-api.yuda.me", "Pop by Yudame"
elif STAGE:
    HOSTNAME, APP_NAME = "pop-stage.yuda.me", "Pop STAGE ENV"
else:
    APP_NAME = "Pop DEV ENV"
    try:
        HOSTNAME = socket.gethostname()
    except:
        HOSTNAME = 'localhost'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# APPLICATIONS
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
    'corsheaders',
    'storages',
    'django_extensions',
    'djmoney',
    'request',
    'social_django',
    'pinax.referrals',
    # 'analytical',
    # 'timezone_field',
    'widget_tweaks',
    'django_user_agents',
    'debug_toolbar',
    'rest_framework',
    'rest_framework_jwt',
    # 'rest_framework.authtoken',
    'django_filters',
    'simple_history',
    # 'anymail',
    # 'ultracache',
    'fontawesome_5',
]

APPS = [
    'apps.common',
    'apps.user',
    'apps.communication',
    'apps.shop',
    # 'apps.website',
    'apps.production',
    # 'apps.event',
    # 'apps.trello',
    'apps.line_app',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + APPS
SITE_ID = 1

MIDDLEWARE = [
    'apps.common.utilities.django_middleware.APIHeaderMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
] + [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
] + [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'request.middleware.RequestMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'pinax.referrals.middleware.SessionJumpingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# AUTHENTICATION_BACKENDS = [
#     # 'apps.user.auth0backend.Auth0',
#     'django.contrib.auth.backends.ModelBackend',
#     'django.contrib.auth.backends.RemoteUserBackend',
# ]

ROOT_URLCONF = 'settings.urls'

# DATABASES = --> SEE VENDOR OR LOCAL SETTINGS

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

# PASSWORD VALIDATION
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

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': (
#         # 'rest_framework.permissions.IsAdminUser',
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 50,
# }

# JWT_AUTH = {
#     'JWT_PAYLOAD_GET_USERNAME_HANDLER':
#         'auth0authorization.utils.jwt_get_username_from_payload_handler',
#     'JWT_DECODE_HANDLER':
#         'auth0authorization.utils.jwt_decode_token',
#     'JWT_ALGORITHM': 'RS256',
#     'JWT_AUDIENCE': APP_NAME,
#     'JWT_ISSUER': 'https://pop-api.yuda.me/',
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',
# }

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


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'


# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    ('shop', os.path.join(SITE_ROOT, 'apps/shop/static')),
]

# General apps settings

if PRODUCTION or STAGE:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

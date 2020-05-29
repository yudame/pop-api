# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '50 char security key here'

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Pop',
        'USER': 'tomcounsell',
        'PASSWORD': '',
        'HOST':     'localhost',
        'PORT':     '5432',
    }
}


# # PRODUCTION AWS RDS database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# AWS
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = AWS_S3_BUCKET_NAME = 'pop-stage'
AWS_OPTIONS = {
    'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
    'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
    'AWS_STORAGE_BUCKET_NAME': AWS_S3_BUCKET_NAME,
}
AWS_SNS_NAME = ''
AWS_STATIC_URL = 'https://' + AWS_S3_BUCKET_NAME + '.s3.amazonaws.com/'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


# OAUTH AND SOCIAL
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

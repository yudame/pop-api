import os
from settings import LOCAL, STAGE, DEMO, PRODUCTION


# AWS
AWS_OPTIONS = {
    'AWS_ACCESS_KEY_ID' : os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID', ""),
    'AWS_SECRET_ACCESS_KEY' : os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY', ""),
    'AWS_STORAGE_BUCKET_NAME' : os.environ.get('BUCKETEER_BUCKET_NAME', ""),
}


if not LOCAL:
  AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
  MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
  AWS_STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
  STATIC_ROOT = STATIC_URL = AWS_STATIC_URL
  DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
  STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

  # DATABASE
  import dj_database_url
  DATABASES = {'default': dj_database_url.config(), }
  DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'


  #SENDGRID EMAIL BACKEND
  EMAIL_HOST          = 'smtp.sendgrid.net'
  EMAIL_PORT          = 587
  EMAIL_USE_TLS       = True
  EMAIL_HOST_USER     = os.environ.get('SENDGRID_USERNAME')
  EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')


  #MEMCACHED CLOUD RESPONSE CACHEING
  CACHES = {
    "default": {
      "BACKEND": "django_redis.cache.RedisCache",
      "LOCATION": os.environ.get('REDIS_URL'),
      "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
      }
    }
  }

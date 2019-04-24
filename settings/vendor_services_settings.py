import os
from settings import LOCAL, STAGE, DEMO, PRODUCTION


if not LOCAL:

  # AWS
  AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
  AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
  AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

  TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
  TRELLO_API_SECRET = os.environ.get("TRELLO_API_SECRET")
  TRELLO_EXPIRATION = os.environ.get("TRELLO_EXPIRATION")
  TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")


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


# AWS
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_URL = STATIC_ROOT = STATIC_URL = AWS_STATIC_URL
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# DATABASE
import dj_database_url
DATABASES = {'default': dj_database_url.config(), }
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

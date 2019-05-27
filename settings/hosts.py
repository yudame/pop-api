from django.conf import settings
from django_hosts import patterns, host
from django.contrib import admin

admin.autodiscover()
host_patterns = patterns(
    '',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'admin', admin.site.urls, name='admin'),
    # host(r'api', 'subdomains_tutorial.api_urls', name='api'),
)

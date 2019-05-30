from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [

    url(r'^$', RedirectView.as_view(url='/admin/login'), name="home"),
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^trello/', include('apps.trello.urls', namespace='trello')),
]

# Built-In AUTH and ADMIN
admin.autodiscover()
urlpatterns += [
    # path('accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
]

from settings import DEBUG

if DEBUG:
    from django.urls import include, path  # For django versions from 2.0 and up
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns

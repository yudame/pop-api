from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView


urlpatterns = [

    url(r'^$', RedirectView.as_view(url='/accounts/login'), name="home"),
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^trello/', include('apps.trello.urls', namespace='trello')),
]


# Built-In AUTH and ADMIN
admin.autodiscover()
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
]

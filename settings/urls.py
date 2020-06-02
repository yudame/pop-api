from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from settings import DEBUG

urlpatterns = [

    # static page
    # path('', TemplateView.as_view(template_name='home.html'), name="home"),

    # route prefix for urlpatterns in apps/dashboard/urls.py
    # path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    # if using namespace, include app_name = "dashboard" in urls.py

    path('', include('apps.user.urls', namespace='user')),

    path('auth0/', include('apps.user.auth0_urls', namespace='auth0')),

    # path('trello/', include('apps.trello.urls', namespace='trello')),
    path('shop/', include('apps.shop.urls', namespace='shop')),

]

# Django Rest Framework API Docs
# from rest_framework.documentation import include_docs_urls
# API_TITLE, API_DESCRIPTION = "Pop API", ""
# urlpatterns += [
#     path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
# ]


# Built-In AUTH and ADMIN
admin.autodiscover()
admin.site.site_header = "Pop Database"
admin.site.site_title = "Pop"
admin.site.site_url = None
admin.site.index_title = "Content Database"

urlpatterns += [
    path('admin/', admin.site.urls),
]


# SCHEDULED TASKS
# urlpatterns += [
#     url(r'^scheduled/v1/some_script',
#         some_util_file.CompilerView.as_view(),
#         name="some_script"),
# ]


# DEBUG MODE use debug_toolbar
if DEBUG:
    from django.urls import include, path  # For django versions from 2.0 and up
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns


# test Auth0 urls
from apps.common.utilities import auth0authorization

urlpatterns += [
    path('api/public', auth0authorization.public),
    path('api/private', auth0authorization.private),
    path('api/private-scoped', auth0authorization.private_scoped),
    path('', include('django.contrib.auth.urls')),
    path('social_django/', include('social_django.urls')),
]

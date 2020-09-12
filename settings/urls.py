from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from apps.api.urls import api_router
from settings import DEBUG

urlpatterns = [

    # static page
    path('', TemplateView.as_view(template_name='home.html'), name="home"),

    # API
    path('api/', include('apps.api.urls', namespace='api')),

    # route prefix for urlpatterns in apps/dashboard/urls.py
    # path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    # if using namespace, include app_name = "dashboard" in urls.py

    # path('auth', include('apps.user.urls', namespace='user')),

    # path('auth0/', include('apps.user.auth0_urls', namespace='auth0')),

    # path('trello/', include('apps.trello.urls', namespace='trello')),
    path('shop/', include('apps.shop.urls', namespace='shop')),

    path('line_app/', include('apps.line_app.urls', namespace='line_app')),

]


# Webpages AUTH
from django.contrib.auth import views as auth_views
urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    # path('account/create/', account.CreateAccount.as_view(), name='create_account'),
    # path('account/activate/', account.ActivateAccount.as_view(), name='activate_account'),
    path('accounts/', include('django.contrib.auth.urls')),
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

# PLUGINS
urlpatterns += [
    path('referrals/', include("pinax.referrals.urls", namespace="pinax_referrals")),
]

# test Auth0 urls
# from apps.common.utilities import auth0authorization
#
# urlpatterns += [
#     path('api/public', auth0authorization.public),
#     path('api/private', auth0authorization.private),
#     path('api/private-scoped', auth0authorization.private_scoped),
#     path('social_django/', include('social_django.urls')),
# ]

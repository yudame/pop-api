from django.urls import path
from django.views.generic import TemplateView

from apps.user.views import auth0views

app_name = "auth0"

urlpatterns = [

    path('index', TemplateView.as_view(template_name='auth0index.html'), name="auth0index"),
    path('dashboard', auth0views.dashboard, name="auth0dashboard"),
    path('logout', auth0views.logout),

]

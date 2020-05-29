from django.urls import path
from django.views.generic import TemplateView

from apps.user.views import home, account
from apps.user.views.auth import login

app_name = "user"

urlpatterns = [

    # MAIN HOME DASHBOARD
    path('', home.HomeView.as_view(), name='home'),

    # USER ACCOUNT
    path('account', account.AccountView.as_view(), name='account'),
    path('login', login.LoginView.as_view(template_name='account/login.html'), name='login'),

    # HELP
    # path('help', TemplateView.as_view(template_name="help.html"), name='help'),ß

]

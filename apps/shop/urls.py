from django.urls import path

from apps.shop.views import dashboard

app_name = 'shop'

urlpatterns = [

    # MAIN HOME DASHBOARD
    path('', dashboard.DashboardView.as_view(), name='dashboard'),
    path('<slug:shop_slug>', dashboard.DashboardView.as_view(), name='dashboard_with_slug'),

]

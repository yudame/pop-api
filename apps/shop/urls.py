from django.urls import path

from apps.shop.views import dashboard, shop

app_name = 'shop'

urlpatterns = [

    # MAIN HOME DASHBOARD
    path('', dashboard.DashboardView.as_view(), name='dashboard'),
    path('<slug:shop_slug>/', dashboard.DashboardView.as_view(), name='dashboard_with_slug'),

    # path('<slug:shop_slug>/menu/add', menu.AddMenuItemView.as_view(), name='menu_add'),
    path('<shop_id>/setup/', shop.SetupView.as_view(), name='setup'),

]

from django.urls import path

from apps.shop.views import dashboard, setup, shop, menu

app_name = 'shop'

urlpatterns = [

    # MAIN HOME
    path('<slug:shop_slug>/', shop.ShopView.as_view(), name='shop'),
    path('<slug:shop_slug>/menu/', menu.MenuView.as_view(), name='menu'),


    # path('<slug:shop_slug>/menu/add', menu.AddMenuItemView.as_view(), name='menu_add'),

    path('<slug:shop_slug>/dashboard/', dashboard.DashboardView.as_view(), name='dashboard'),
    path('<shop_id>/setup/', setup.SetupView.as_view(), name='setup'),

]

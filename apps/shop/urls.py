from django.urls import path

from apps.shop.views import dashboard, setup, shop, menu, order

app_name = 'shop'

urlpatterns = [

    # MENU AND ORDERS

    path('orders/', order.OrdersView.as_view(), name='orders'),
    path('orders/<order_id>/', order.OrderView.as_view(), name='order'),
    path('orders/<order_id>/confirm/', order.ConfirmOrderView.as_view(), name='confirm_order'),

    path('<slug:shop_slug>/menu/', menu.MenuView.as_view(), name='menu'),

    # MAIN HOME
    path('<slug:shop_slug>/', shop.ShopView.as_view(), name='shop'),

    # path('<slug:shop_slug>/menu/add', menu.AddMenuItemView.as_view(), name='menu_add'),
    path('<slug:shop_slug>/dashboard/', dashboard.DashboardView.as_view(), name='dashboard'),
    path('<shop_id>/setup/', setup.SetupView.as_view(), name='setup'),

]

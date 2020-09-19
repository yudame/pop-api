from rest_framework import routers

from apps.api.views import item, menu

# API V2

app_name = 'api'
api_router = routers.DefaultRouter()

api_router.register(r'menus', menu.MenuViewSet)
api_router.register(r'items', item.ItemViewSet)

urlpatterns = api_router.urls

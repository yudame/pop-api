from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, authentication, permissions

from apps.api.serializers.menu import MenuSerializer
from apps.shop.models import Menu

class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    LIST endpoints:

    - `/menus/` returns all menus.

    GET endpoint:

    - `/menus/123/` returns item object where item_id=123

    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    # filterset_fields = ('shop', )
    authentication_classes = [authentication.BasicAuthentication, ]
    # permission_classes = [WildWest | permissions.IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.all()

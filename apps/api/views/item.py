from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, authentication, permissions

from apps.api.serializers.item import ItemSerializer
from apps.shop.models import Item

class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    LIST endpoints:

    - `/items/` returns all items.

    GET endpoint:

    - `/items/123/` returns item object where item_id=123

    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    # filterset_fields = ('shop', 'menu_category', )
    authentication_classes = [authentication.BasicAuthentication, ]
    # permission_classes = [WildWest | permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.all()


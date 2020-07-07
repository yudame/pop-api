from abc import ABC

from apps.shop.models import Shop


class Delivery(ABC):
    shop = Shop.objects.first()



from rest_framework import serializers
from typing import Dict, Any
from apps.shop.models import Item


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price_amount = serializers.SerializerMethodField()

    def get_price_amount(self, obj):
        return obj.price.amount if obj.price else None

def get_serialized_item(item: Item) -> Dict[str, Any]:
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price_amount': item.price.amount if item.price else None,
    }

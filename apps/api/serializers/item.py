from rest_framework import serializers

from apps.shop.models import Item


class ItemSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    # menu_section_id = serializers.IntegerField()


from typing import Dict, Any

def fast_serialize_item(item: Item) -> Dict[str, Any]:
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
    }

def fast_minimal_serialize_item(item: Item) -> Dict[str, Any]:
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
    }

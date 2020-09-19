from rest_framework import serializers
from typing import Dict, Any

from apps.api.serializers.item import get_serialized_item
from apps.shop.models import Menu
from apps.shop.models import MenuSection


class MenuSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    header_text = serializers.CharField()
    footer_text = serializers.CharField()
    menu_sections = serializers.SerializerMethodField()

    def get_menu_sections(self, obj):
        return [
            get_serialized_menu_section(menu_section)
            for menu_section in obj.menu_sections.order_by('display_on_menu_position')
        ]

def get_serialized_menu(menu: Menu) -> Dict[str, Any]:
    return {
        'id': menu.id,
        'header_text': menu.header_text,
        'footer_text': menu.footer_text,
        'menu_sections': [
            get_serialized_menu_section(menu_section)
            for menu_section in menu.menu_sections.order_by('display_on_menu_position')
        ],
    }


def get_serialized_menu_section(menu_section: MenuSection) -> Dict[str, Any]:
    return {
        'id': menu_section.id,
        'name': menu_section.name,
        'items': [
            get_serialized_item(item)
            for item in menu_section.items.order_by('display_on_menu_position')
        ],
    }

from django.contrib import admin

from apps.common.admin import MyModelAdmin
from apps.shop.models import Shop, Menu, MenuCategory, MenuSection, Item
from apps.shop.models import AddonGroup, ItemAddonGroups, ItemAddonGroupMemberships


@admin.register(Shop)
class ShopAdmin(MyModelAdmin):
    list_display = (
        # 'id',
        'name',
        'owner',
        # 'description',
        'address',
        'timezone',
        # 'longitude',
        # 'latitude',
        # 'created_at',
        # 'modified_at',
        # 'contact_name',
        # 'contact_phone_number',
        # 'contact_email',
        # 'base_language',
        # 'languages',
        # 'square_logo_src',
        # 'facebook_href',
        # 'instagram_href',
        # 'google_maps_href',
        # 'trip_advisor_href',
        'is_ghost_location',
        'currency',
    )
    list_filter = (
        'address',
        'created_at',
        'modified_at',
        'owner',
        'is_ghost_location',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Menu)
class MenuAdmin(MyModelAdmin):
    list_display = (
        # 'id',
        'created_at',
        'modified_at',
        'shop',
        'header_text',
        'footer_text',
        'breakfast_open_time',
        'breakfast_close_time',
        'brunch_open_time',
        'brunch_close_time',
        'lunch_open_time',
        'lunch_close_time',
        'dinner_open_time',
        'dinner_close_time',
    )
    list_filter = ('created_at', 'modified_at', 'shop')
    date_hierarchy = 'created_at'


@admin.register(MenuCategory)
class MenuCategoryAdmin(MyModelAdmin):
    list_display = (
        # 'id',
        'name',
        'parent',
        'icon',
    )
    list_filter = ('parent',)
    search_fields = ('name',)


@admin.register(MenuSection)
class MenuSectionAdmin(MyModelAdmin):
    list_display = (
        # 'id',
        'name',
        'custom_icon',
        'menu',
        'menu_category',
        'is_display_on_menu',
        'display_on_menu_position',
    )
    list_filter = ('menu', 'menu_category', 'is_display_on_menu')
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(MyModelAdmin):
    list_display = (
        # 'id',
        # 'valid_at',
        # 'expired_at',
        # 'created_at',
        # 'modified_at',
        # 'published_at',
        # 'edited_at',
        # 'unpublished_at',
        'name',
        # 'description',
        # 'image',
        'menu',
        'menu_section',
        # 'calories_count',
        'options_required_count',
        'is_option',
        # 'option_price_currency',
        'option_price',
        'is_display_on_menu',
        'display_on_menu_position',
        # 'price_currency',
        'price',
        'unavailable_periods',
    )
    list_filter = (
        # 'valid_at',
        # 'expired_at',
        # 'created_at',
        # 'modified_at',
        # 'published_at',
        # 'edited_at',
        # 'unpublished_at',
        # 'image',
        'menu',
        'menu_section',
        'is_option',
        'is_display_on_menu',
    )
    raw_id_fields = (
        'notes',
        'alt_images',
        'items_for_option',
        'groups_of_addons',
        'groups_as_addon',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(AddonGroup)
class AddonGroupAdmin(MyModelAdmin):
    list_display = (
        # 'id',
        # 'valid_at',
        # 'expired_at',
        # 'created_at',
        # 'modified_at',
        # 'published_at',
        # 'edited_at',
        # 'unpublished_at',
        'name',
        # 'description',
        # 'image',
    )
    list_filter = (
        # 'valid_at',
        # 'expired_at',
        # 'created_at',
        # 'modified_at',
        # 'published_at',
        # 'edited_at',
        # 'unpublished_at',
        # 'image',
    )
    raw_id_fields = ('notes',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(ItemAddonGroups)
class ItemAddonGroupsAdmin(MyModelAdmin):
    list_display = (
        # 'id',
        # 'created_at',
        # 'modified_at',
        'item',
        'addon_group',
        'addon_max_count',
        'addon_free_count',
        # 'standard_price_currency',
        'standard_price',
    )
    list_filter = ('created_at', 'modified_at', 'item', 'addon_group')
    raw_id_fields = ('notes',)
    date_hierarchy = 'created_at'


@admin.register(ItemAddonGroupMemberships)
class ItemAddonGroupMembershipsAdmin(MyModelAdmin):
    list_display = (
        # 'id',
        # 'created_at',
        # 'modified_at',
        'item',
        'addon_group',
        'is_never_free',
        # 'addon_price_currency',
        'addon_price',
    )
    list_filter = (
        # 'created_at',
        # 'modified_at',
        'item',
        'addon_group',
        'is_never_free',
    )
    raw_id_fields = ('notes',)
    date_hierarchy = 'created_at'
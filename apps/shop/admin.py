from django.contrib import admin
from apps.shop.models import Shop, Menu, MenuCategory, MenuSection, Item


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

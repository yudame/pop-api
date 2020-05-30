from django.contrib import admin
from apps.shop.models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

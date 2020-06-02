from django.contrib import admin
from apps.production.models import Good, Supplier


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    pass

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass

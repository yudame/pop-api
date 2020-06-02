from django.db import models

from apps.common.behaviors import Contactable


class Supplier(Contactable, models.Model):

    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=50)


    # META
    class Meta:
        ordering = ('name',)
        unique_together = ('shop', 'name')

from django.db import models
from djmoney.models.fields import MoneyField

from apps.common.behaviors import Timestampable, Annotatable


class OrderItem(Timestampable, Annotatable, models.Model):

    order = models.ForeignKey('shop.Order', null=False, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey('shop.Item', null=True, on_delete=models.PROTECT, related_name='order_items')

    quantity = models.DecimalField(default=1, decimal_places=2, max_digits=8)

    is_ad_hoc_item = models.BooleanField(default=False)
    ad_hoc_name = models.CharField(max_length=100, default="", blank=True)
    ad_hoc_price = MoneyField(max_digits=8, decimal_places=2, null=True, blank=True, default_currency='THB')


    # MODEL PROPERTIES

    # MODEL FUNCTIONS

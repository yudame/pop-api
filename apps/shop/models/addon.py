from django.db import models
from djmoney.models.fields import MoneyField
from apps.common.behaviors import Timestampable, Publishable, Expirable, Annotatable
from apps.shop.models.item import Item


class AddonType(Timestampable, Publishable, Expirable, Annotatable, models.Model):

    addon_max_count = models.SmallIntegerField(null=True, blank=True,
                                               help_text='maxiumum number of addons allowed (eg. 10 salad toppings)')
    addon_free_count = models.SmallIntegerField(null=True, blank=True,
                                                help_text='number of free addons allowed (eg. 1 for salad dressing)')
    standard_price = MoneyField(max_digits=8, decimal_places=2, null=True, blank=True, default_currency='THB',
                                help_text='set price for all extra addons (eg. $2 for extra cheese)')



class Addon(Item):

    addon_type = models.ForeignKey('shop.AddonType', on_delete=models.CASCADE, related_name='addons')
    # pray to God this doesn't become a M2M field

    addon_price = MoneyField(max_digits=8, decimal_places=2, null=True, blank=True, default_currency='THB',
                             help_text='price when not free')

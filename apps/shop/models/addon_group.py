from django.db import models
from djmoney.models.fields import MoneyField
from apps.common.behaviors import Timestampable, Publishable, Expirable, Annotatable


class AddonGroup(Timestampable, Publishable, Expirable, Annotatable, models.Model):
    """
    a grouping of item addons
    example: side dishes, pizza toppings, salad dressings
    """
    name = models.CharField(max_length=140, blank=False)
    description = models.TextField(default='', blank=True)
    image = models.OneToOneField('common.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='addon_group')


class ItemAddonGroups(Timestampable, Annotatable, models.Model):
    """
    relationship between an item and it's addons
    example: first 5 of these salad toppings are free, then $1 each for max 10 toppings
    """
    item = models.ForeignKey('shop.Item', on_delete=models.CASCADE, related_name='item_addon_groups')
    addon_group = models.ForeignKey('shop.AddonGroup', on_delete=models.CASCADE, related_name='item_addon_groups')

    addon_max_count = models.SmallIntegerField(null=True, blank=True,
        help_text='maxiumum number of addons allowed (eg. 10 salad toppings)')
    addon_free_count = models.SmallIntegerField(null=True, blank=True,
        help_text='number of free addons allowed (eg. 1 for salad dressing)')
    standard_price = MoneyField(max_digits=8, decimal_places=2, null=True, blank=True, default_currency='THB',
        help_text='set price for all extra addons (eg. all toppings are $1 extra each)')


class ItemAddonGroupMemberships(Timestampable, Annotatable, models.Model):
    """
    an items membership within an addon group
    example: mushrooms as a pizza topping cost $1
    """
    item = models.ForeignKey('shop.Item', on_delete=models.CASCADE, related_name='item_addon_group_memberships')
    addon_group = models.ForeignKey('shop.AddonGroup', null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='item_addon_group_memberships')
    # pray to God this doesn't become a M2M field
    is_never_free = models.BooleanField(default=False)
    addon_price = MoneyField(max_digits=8, decimal_places=2, null=True, blank=True, default_currency='THB',
        help_text='price when not automatically free')

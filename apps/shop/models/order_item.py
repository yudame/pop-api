import logging

from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from apps.common.behaviors import Timestampable, Annotatable


class OrderItem(Timestampable, Annotatable, models.Model):

    order = models.ForeignKey('shop.Order', null=False, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey('shop.Item', null=True, on_delete=models.PROTECT, related_name='order_items')

    option_items = models.ManyToManyField('shop.Item', related_name='order_items_as_option')
    # note: duplicates in options and addons are ok, represents quantity
    addon_items = models.ManyToManyField('shop.Item', related_name='order_items_as_addon')

    quantity = models.DecimalField(default=1, decimal_places=2, max_digits=8)

    is_ad_hoc_item = models.BooleanField(default=False)
    ad_hoc_name = models.CharField(max_length=100, default="", blank=True)
    ad_hoc_price = MoneyField(max_digits=8, decimal_places=2, null=True, blank=True, default_currency='THB')


    # MODEL PROPERTIES

    @property
    def price(self):
        logging.debug("calculating price .. again")
        if self.ad_hoc_price:
            return self.ad_hoc_price.amount * self.quantity

        total_amount = self.item.price.amount

        # add options
        for option_item in self.option_items.all():
            total_amount += (
                    option_item.option_price.amount
                    or option_item.price.amount
            )

        # add price.amount for each addon, excluding free addons
        free_counters = {}
        for addon_item in self.addon_items.all():
            item_addon_group_membership = addon_item.item_addon_group_memberships.filter(
                addon_group__item_id=self.item_id
            ).order_by('custom_addon_price')
            # order by custom price so free_addon_count is applied to non-custom items first

            # if never free, find price by hierarchy
            if item_addon_group_membership.is_never_free:
                total_amount += (
                        item_addon_group_membership.custom_addon_price.amount
                        or item_addon_group_membership.addon_group.per_addon_price.amount
                        or item_addon_group_membership.item.price.amount
                )
                continue

            # check against possible addon_free_count and add price if/when necessary
            addon_group = item_addon_group_membership.addon_group
            if addon_group.id in free_counters:
                free_counters[addon_group.id] -= 1
            else:
                free_counters[addon_group.id] = addon_group.addon_free_count or 0
                free_counters[addon_group.id] -= 1
            if free_counters[addon_group.id] < 0:
                total_amount += (
                        item_addon_group_membership.custom_addon_price.amount
                        or item_addon_group_membership.addon_group.per_addon_price.amount
                        or item_addon_group_membership.item.price.amount
                )

        return Money(
            round(total_amount * self.quantity, 2),  # finally round off to nearest 2 decimal places
            self.item.price.currency
        )

    # MODEL FUNCTIONS
    def get_cart_index_string(self):
        index_string = f"i{self.item.id}"
        for option_item in self.option_items.order_by('id'):
            index_string += f"+o{option_item.id}"
        for addon_item in self.addon_items.order_by('id'):
            index_string += f"+a{addon_item.id}"
        return index_string

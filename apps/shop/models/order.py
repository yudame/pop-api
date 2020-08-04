from django.contrib.postgres.fields import JSONField
from django.db import models
from djmoney.money import Money
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField
from apps.common.behaviors import Timestampable, Annotatable


# STATUS_CHOICES = [
#     ('', 'no status'),
#     (DRAFT, 'draft'),
#     (PLACED, 'order placed'),
#     (CUSTOMER_CANCELLED, 'customer cancelled'),
#     (DELIVERY_REJECTED, 'delivery rejected'),
#     (DELIVERY_CONFIRMED, 'delivery confirmed'),
#     (SHOP_REJECTED, 'shop rejected'),
#     (SHOP_CONFIRMED, 'shop confirmed'),
#     (SHOP_COMPLETE, 'shop complete'),
#     (DELIVERY_START, 'delivery start'),
#     (DELIVERY_COMPLETE, 'delivery complete'),
#     (AUTO_FINALIZED, 'finalized (auto)'),
#     (CUSTOMER_FINALIZED, 'finalized (customer comfirmed)'),
#     (CUSTOMER_RATED, 'customer rating'),
#     (CUSTOMER_COMPLAINT, 'customer complaint'),
#     (SYSTEM_REJECTED_ERROR, 'system rejected (error)'),
#     (SYSTEM_REJECTED_FRAUD, 'system rejected (fraud)'),
#     (PROCESSING, 'processing... (locked)'),
# ]
from settings import AUTH_USER_MODEL


class Order(Timestampable, Annotatable, models.Model):

    # customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    # shop = models.ForeignKey('shop.Shop', on_delete=models.PROTECT, related_name='orders')

    line_channel_membership = models.ForeignKey('line_app.LineChannelMembership', null=True,
                                                on_delete=models.SET_NULL, related_name='orders')

    items = models.ManyToManyField('shop.Item', blank=True, through='shop.OrderItem', related_name='orders')
    #  OrderItem is annotatable, has many discounts, quantity(decimal?), and no unique_together constraints

    # ad_hoc_items = models.ManyToManyField('shop.AdHocItem', blank=True, related_name='orders', through='order.OrderAdHocItem')
    #  OrderItem is annotatable and authorable, , has quantity and no unique_together constraints

    # promotions = models.ManyToManyField('shop.Promotion', through='OrderPromotion', blank=True, related_name='orders')
    # discounts = models.ManyToManyField('shop.Discounts', related_name='orders', blank=True)
    # fees = models.ManyToManyField('shop.Fee', through='OrderFee', blank=True, related_name='orders')

    # MONEY
    # total_money_to_pay = MoneyField(max_digits=8, decimal_places=2, null=True, default_currency='THB')

    # payments = other model. an order can have many payments if split (or one fails)
    #     payment_method = models.CharField(max_length=20)
    #     payment_at = models.DateTimeField(null=True, blank=True)  # is_confirmed
    # total_money_payed = function of sum of payments with payment_at (ie. confirmed)

    # # todo: move delivery info to order.Delivery model. a delivery is locatable and annotatable
    # # todo: a delivery has a unique set of statuses only applicable to delivery-type orders
    # estimated_delivery_at = models.DateTimeField(null=True, blank=True)
    # delivery_at = models.DateTimeField(null=True, blank=True)
    # address (locatable)

    # # PROCESS
    # previous_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default='')  # for context of where it came from
    # current_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=DRAFT)  # know current state
    # next_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=PLACED)  # move the order towards a goal
    status_log = JSONField(default=dict, blank=True, null=True)
    draft_cart = JSONField(default=dict, blank=True, null=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # please do not set dates in the future!

    # MODEL PROPERTIES

    @property
    def items_total_price_amount(self):
        return sum([
            order_item.price.amount for order_item in self.order_items.all()
        ])

    @property
    def items_total_price(self):
        return Money(self.items_total_price_amount, self.order_items.first().price.currency)


    @property
    def is_completed(self) -> bool:
        from django.utils.timezone import now
        return True if self.completed_at and self.completed_at < now() else False

    @is_completed.setter
    def is_completed(self, value: bool):
        from django.utils.timezone import now
        if value is True:
            self.completed_at = now()
        elif value is False and self.is_completed:
            self.completed_at = None

    # MODEL FUNCTIONS

    def get_cart_dict(self):
        cart_dict = dict()
        for order_item in self.order_items.all():
            key = order_item.get_cart_index_string()
            cart_dict[key] = {
                'order_item_id': str(order_item.id),
                'item_id': str(order_item.item.id),
                'name': str(order_item.item.name),
                'quantity': int(order_item.quantity),
                'note': str(order_item.notes.first().text if order_item.notes.count() else ""),
                'price_amount': str(order_item.price.amount)
            }
            # todo: add promotions, discounts, fees
        return cart_dict


    def __str__(self):
        return f"Order for {self.line_channel_membership}"

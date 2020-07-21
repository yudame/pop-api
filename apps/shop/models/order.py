from django.contrib.postgres.fields import JSONField
from django.db import models
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

    line_channel_membership = models.OneToOneField('line_app.LineChannelMembership', null=True,
                                                   on_delete=models.SET_NULL)

    items = models.ManyToManyField('shop.Item', blank=True, through='shop.OrderItem', related_name='orders')
    #  OrderItem is annotatable, has many discounts, quantity(decimal?), and no unique_together constraints

    # ad_hoc_items = models.ManyToManyField('shop.AdHocItem', blank=True, related_name='orders', through='order.OrderAdHocItem')
    #  OrderItem is annotatable and authorable, , has quantity and no unique_together constraints

    # promotions = models.ManyToManyField('shop.Promotion', through='OrderPromotion', blank=True, related_name='orders')
    # discounts = models.ManyToManyField('shop.Discounts', related_name='orders', blank=True)
    # fees = models.ManyToManyField('shop.Fee', through='OrderFee', blank=True, related_name='orders')

    # MONEY
    # total_to_pay = MoneyField(max_digits=8, decimal_places=2, null=True, default_currency='THB')

    # payments = other model. an order can have many payments if split (or one fails)
    #     payment_method = models.CharField(max_length=20)
    #     payment_at = models.DateTimeField(null=True, blank=True)  # is_confirmed
    # total_payed = function of sum of payments with payment_at (ie. confirmed)

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


    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def __str__(self):
        return f"Order for {self.line_channel_membership}"

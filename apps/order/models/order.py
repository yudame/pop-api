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

    customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    shop = models.ForeignKey('shop.Shop', on_delete=models.PROTECT, related_name='orders')
    # items = models.ManyToManyField('shop.Item', blank=True, related_name='orders', through='order.OrderItem')
    #  order_item is annotatable, has many discounts, quantity(decimal?), and no unique_together constraints

    # # PROCESS
    # previous_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default='')  # for context of where it came from
    # current_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=DRAFT)  # know current state
    # next_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=PLACED)  # move the order towards a goal
    # # timestamp or activity log for each status

    # # todo: move delivery info to order.Delivery model. a delivery is locatable and annotatable
    # # todo: a delivery has a unique set of statuses only applicable to delivery-type orders
    # estimated_delivery_at = models.DateTimeField(null=True, blank=True)
    # delivery_at = models.DateTimeField(null=True, blank=True)
    # address (locatable)

    # MONEY
    # discounts = models.ManyToManyField('order.Discounts', related_name='orders', blank=True)
    # total_charge = MoneyField(max_digits=8, decimal_places=2, null=True, default_currency='THB')

    # # todo: move payment info to other model. an order can have many payments if split or one fails
    # total_payment = MoneyField(max_digits=8, decimal_places=2, null=True, default_currency='THB')
    # payment_method = models.CharField(max_length=20)
    # payment_at = models.DateTimeField(null=True, blank=True)

    promotions = models.ManyToManyField('Promotion', through='OrderPromotion', blank=True, related_name='orders')

    fees = models.ManyToManyField('Fee', through='OrderFee', blank=True, related_name='orders')

    # HISTORY MANAGER
    history = HistoricalRecords()

    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def __str__(self):
        return f"{self.shop.name} Menu"

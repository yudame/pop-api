from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from djmoney.money import Money
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField
from apps.common.behaviors import Timestampable, Annotatable

DRAFT, PLACED, CUSTOMER_CANCELLED, SHOP_REJECTED, SHOP_CONFIRMED, SHOP_COMPLETE, EXPIRED = range(7)

STATUS_CHOICES = [
    (None, 'no status'),
    (DRAFT, 'draft'),
    (PLACED, 'order placed'),
    (CUSTOMER_CANCELLED, 'customer cancelled'),
    (SHOP_REJECTED, 'shop rejected'),
    (SHOP_CONFIRMED, 'shop confirmed'),
    (SHOP_COMPLETE, 'shop complete'),
    # (SHOP_CANCELLED, 'shop cancelled'),
    (EXPIRED, 'expired or abandoned'),

    # (DELIVERY_REJECTED, 'delivery rejected'),
    # (DELIVERY_CONFIRMED, 'delivery confirmed'),
    # (DELIVERY_START, 'delivery start'),
    # (DELIVERY_COMPLETE, 'delivery complete'),
    # (AUTO_FINALIZED, 'finalized (auto)'),
    # (CUSTOMER_FINALIZED, 'finalized (customer comfirmed)'),
    # (CUSTOMER_RATED, 'customer rating'),
    # (CUSTOMER_COMPLAINT, 'customer complaint'),
    # (SYSTEM_REJECTED_ERROR, 'system rejected (error)'),
    # (SYSTEM_REJECTED_FRAUD, 'system rejected (fraud)'),
    # (PROCESSING, 'processing... (locked)'),
]


class Order(Timestampable, Annotatable, models.Model):
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

    # PROCESS
    previous_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=None, null=True,
                                                       blank=True)  # for context of where it came from
    current_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=DRAFT, null=True,
                                                      blank=True)  # know current state
    next_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=PLACED, null=True,
                                                   blank=True)  # move the order towards a goal

    status_log = JSONField(default=dict, blank=True, null=True)
    draft_cart = JSONField(default=dict, blank=True, null=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # at end of lifecycle, see status history for how/why

    # MODEL PROPERTIES

    @property
    def shop(self):
        return self.line_channel_membership.line_channel.shop

    @property
    def items_total_price_amount(self):
        price_amount_sum = sum([
            order_item.price.amount for order_item in self.order_items.all()
        ])
        return round(price_amount_sum, 2)

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

    @property
    def total_item_count(self):
        return int(sum([
            oi.quantity if (oi.quantity % 1 == 0) else 1
            for oi in self.order_items.all()
        ]))

    @property
    def is_ready_for_checkout(self):
        return False if any([
            self.is_completed,
            self.total_item_count == 0,
        ]) else True

    # MODEL FUNCTIONS

    def get_cart_dict(self):
        cart_dict = dict()
        # note: only order items can have keys starting with "i"
        for order_item in self.order_items.all():
            key = order_item.get_cart_index_string()
            cart_dict[key] = {
                'order_item_id': str(order_item.id),
                'item_id': str(order_item.item.id),
                'name': str(order_item.item.name),
                'quantity': int(order_item.quantity),
                'note': str(order_item.notes.first().text if order_item.notes.count() else ""),
                'price_amount': str(int(round(order_item.price.amount, 0)))
            }
        cart_dict["total_item_count"] = str(self.total_item_count),
        cart_dict["total_price_amount"] = str(int(round(self.items_total_price_amount, 2))),
        cart_dict["ready_for_checkout"] = self.is_ready_for_checkout,
        # todo: add promotions, discounts, fees
        return cart_dict

    def set_status(self, new_status, next=None, override_datetime: datetime = datetime.now()):
        if new_status not in dict(STATUS_CHOICES) or (next and next not in dict(STATUS_CHOICES)):
            raise Exception("invalid status provided")
        if self.current_status != new_status:
            self.previous_status = self.current_status
        self.current_status = new_status
        self.next_status = next or None
        if isinstance(override_datetime, datetime):
            self.status_log.update({
                str(override_datetime): f"{self.previous_status}->{self.current_status}->{self.next_status}"
            })
        if self.current_status in [
            CUSTOMER_CANCELLED, SHOP_REJECTED, SHOP_COMPLETE, EXPIRED
        ] or (self.current_status is None and self.previous_status is not None):
            self.is_completed = True

    def get_absolute_url(self):
        return reverse('shop:order', kwargs={'order_id': self.id})

    def __str__(self):
        return f"Order for {self.line_channel_membership}"

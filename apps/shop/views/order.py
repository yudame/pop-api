from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import View
from apps.shop.views.login_mixins import LineRichMenuLoginMixin, OTPLoginMixin
from apps.common.utilities.multithreading import start_new_thread
from apps.shop.models import Order, OrderItem
from apps.shop.models.order import DRAFT, PLACED, SHOP_CONFIRMED, SHOP_COMPLETE
from apps.shop.views.shop import ShopViewMixin
from settings import HOSTNAME


class OrderException(Exception):
    pass


def update_order(order: Order, send_order_summary=False) -> Order:

    if order.current_status is DRAFT:
        # update order_items based on order.draft_cart

        order_item_ids_processed = []
        for cart_index_string, cart_item in order.draft_cart.items():
            if not cart_index_string.startswith("i"):
                continue

            if 'item_id' not in cart_item:
                raise OrderException("missing item_id in cart item")
            if 'quantity' not in cart_item:
                raise OrderException("missing quantity in cart item")

            order_item = OrderItem.objects.none()
            if 'order_item_id' in cart_item:
                if cart_item['order_item_id'] in order_item_ids_processed:
                    raise OrderException("duplicate order_item_id found")
                if cart_item['order_item_id']:
                    order_item = OrderItem.objects.filter(id=cart_item['order_item_id']).first()

            if all([
                not order_item,
                cart_item.get('item_id'),
                cart_item.get('quantity'),
            ]):
                order_item = OrderItem.objects.create(order=order, item_id=cart_item['item_id'])

            order_item.quantity = Decimal(cart_item['quantity'])

            if len(cart_item.get('note', "")):
                note = order_item.notes.first()
                if note:
                    note.text = cart_item['note']
                    note.save()
                else:
                    order_item.add_note(cart_item['note'])

            order_item.save()
            order_item_ids_processed.append(order_item.id)

        order.order_items.exclude(id__in=order_item_ids_processed).delete()
        order.save()

    if send_order_summary and order.is_ready_for_checkout:
        # send order summary to customer
        order.line_channel_membership.send_order_summary(order)

    if order.current_status is PLACED and order.next_status is SHOP_CONFIRMED:
        pursue_shop_confirmation(order)

    return order


@start_new_thread
def async_update_order(order: Order, send_order_summary=False):
    update_order(order, send_order_summary)
    from django.db import connection
    connection.close()

def pursue_shop_confirmation(order: Order):

    confirm_order_route = reverse('shop:confirm_order', kwargs={'order_id':order.id})
    login_kwargs = {
        'username': order.shop.owner.username,
        'otp': order.shop.owner.get_otp(num_digits=8),
    }

    confirm_order_url = f'https://{HOSTNAME}{confirm_order_route}?{urlencode(login_kwargs)}'

    # if order.shop.has_pushover:
    from apps.communication.views.pushover import Pushover
    p = Pushover()
    p.send_urgent_order_to_shop(order, confirm_order_url=confirm_order_url)


class OrdersView(LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):
    def get(self, request, *args, **kwargs):
        self.context.update({
            'placed_orders': self.shop.orders.filter(current_status=PLACED, next_status=SHOP_CONFIRMED),
            'confirmed_orders': self.shop.orders.filter(current_status=SHOP_CONFIRMED, next_status=SHOP_COMPLETE),
            'completed_orders': self.shop.orders.filter(Q(current_status=SHOP_COMPLETE) | Q(previous_status=SHOP_COMPLETE)),
        })
        return render(request, 'orders.html', self.context)


class OrderView(LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):

    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        # if order not in self.shop.orders.all():
        #     return HttpResponseNotFound()  # 404
        self.context['order'] = order
        return render(request, 'order.html', self.context)


class ConfirmOrderView(OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):

    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        order.set_status(SHOP_CONFIRMED, next=SHOP_COMPLETE)
        order.line_channel_membership.send_order_confirmation(order)
        order.save()
        redirect('shop:order', order_id=order.id)

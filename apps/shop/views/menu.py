import json
import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.shortcuts import render, redirect
from rest_framework import status

from apps.common.utilities.multithreading import start_new_thread
from apps.line_app.models import LineChannelMembership
from apps.shop.models import Shop, Order, OrderItem
from apps.shop.views.login_mixins import LineRichMenuLoginMixin, OTPLoginMixin
from apps.shop.views.shop import ShopViewMixin


# todo: move to views/order.py
@start_new_thread
def async_update_order(order: Order, cart_item_list: list, send_order_summary=True) -> Order:
    order_item_ids_processed = []

    for cart_item in cart_item_list:
        if 'item_id' not in cart_item:
            raise Exception("missing item_id in cart item")
        if 'quantity' not in cart_item:
            raise Exception("missing quantity in cart item")

        order_item = OrderItem.objects.none()
        if 'order_item_id' in cart_item:
            if cart_item['order_item_id'] in order_item_ids_processed:
                raise Exception("duplicate order_item_id found")
            if cart_item['order_item_id']:
                order_item = OrderItem.objects.filter(id=cart_item['order_item_id']).first()

        if not order_item:
            order_item = OrderItem.objects.create(order=order)

        if cart_item.get('item_id') and cart_item.get('quantity'):
            order_item.item_id = cart_item['item_id']
            order_item.quantity = Decimal(cart_item['quantity'])

        order_item.save()
        order_item_ids_processed.append(order_item.id)

    order.order_items.exclude(id__in=order_item_ids_processed).delete()
    order.draft_cart = {'cart_item_list': order.get_cart_list()}
    order.save()
    if send_order_summary:
        order.line_channel_membership.send_order_summary(order)
    from django.db import connection
    connection.close()


class MenuView(LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        line_channel_membership = LineChannelMembership.objects.filter(
            line_user_profile__user=request.user,
            line_channel__shop_id=self.shop.id
        ).first()
        if not line_channel_membership:
            messages.warning(request, "Connect with Line to view menu.")
            return redirect('shop:shop', shop_slug=self.shop.slug)
        request.session['line_channel_membership_id'] = line_channel_membership.id
        order, o_created = Order.objects.get_or_create(line_channel_membership=line_channel_membership,
                                                       completed_at=None)
        request.session['order_id'] = order.id

        self.context.update({
            "line_channel_membership": line_channel_membership,
            "shopping_cart_json": json.dumps(order.draft_cart.get('cart_item_list', [])),
            "total_price_amount": order.items_total_price_amount,
        })
        return render(request, 'menu.html', self.context)

    def post(self, request, *args, **kwargs):  # html interface
        logging.debug(request.POST)

        line_channel_membership_id = request.POST.get('line_channel_membership_id',
                                                      request.session.get('line_channel_membership_id'))
        if not line_channel_membership_id:
            return JsonResponse({'error': "line_channel_membership_id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        order, o_created = Order.objects.get_or_create(line_channel_membership_id=line_channel_membership_id,
                                                       completed_at=None)

        cart_item_list = json.loads(request.POST.get('cart'))
        if not cart_item_list or not isinstance(cart_item_list, list):
            return JsonResponse({'error': "sorry, I can only take a list"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        order.draft_cart = {
            'cart_item_list': cart_item_list,
        }

        if request.POST.get('checkout', "false").lower() == "true":
            logging.debug("ready for checkout!")
            async_update_order(order, cart_item_list, send_order_summary=True)
        else:  # prevent race condition bc async function will also change order and save
            order.save()

        return JsonResponse({'success': "order saved"}, status=status.HTTP_202_ACCEPTED)

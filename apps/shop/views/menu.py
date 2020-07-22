import json
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from rest_framework import status

from apps.line_app.models import LineChannelMembership
from apps.shop.models import Shop, Order
from apps.shop.views.login_mixins import LineRichMenuLoginMixin, OTPLoginMixin
from apps.shop.views.shop import ShopViewMixin


# todo: move me to views/order.py
def update_order(order: Order, cart_item_list: list) -> Order:
    for cart_item in cart_item_list:
        pass
    return order



class MenuView(LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):

    def get(self, request, *args, **kwargs):
        line_channel_membership = LineChannelMembership.objects.get(
            line_user_profile__user=request.user,
            line_channel__shop_id=self.shop.id
        )
        request.session['line_channel_membership_id'] = line_channel_membership.id
        order, o_created = Order.objects.get_or_create(line_channel_membership=line_channel_membership, completed_at=None)
        request.session['order_id'] = order.id

        self.context.update({
            "line_channel_membership": line_channel_membership,
            "shopping_cart_json": json.dumps(order.get_cart_list()),
            "total_price_amount": order.items_total_price_amount,
        })
        return render(request, 'menu.html', self.context)

    def post(self, request, *args, **kwargs): #html interface
        logging.debug(request.POST)

        line_channel_membership = request.POST.get('line_channel_membership_id',
                                                   request.session.get('line_channel_membership_id'))
        if not line_channel_membership:
            return JsonResponse({'error': "line_channel_membership_id"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        order, o_created = Order.objects.get_or_create(line_channel_membership=line_channel_membership, completed_at=None)

        cart_item_list = json.loads(request.POST.get('cart'))
        if not cart_item_list or not isinstance(cart_item_list, list):
            return JsonResponse({'error': "sorry, I can only take a list"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        order = update_order(order, cart_item_list)
        order.save()
        return JsonResponse({'success': "order saved"}, status=status.HTTP_202_ACCEPTED)

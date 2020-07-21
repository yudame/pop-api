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
def update_order(order: Order, cart_items: dict):
    for order_item_id, order_item in cart_items.items():
        pass



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
            "shopping_cart_json": json.dumps(order.get_cart_dict()),
        })
        return render(request, 'menu.html', self.context)


    def post(self, request, *args, **kwargs): #html interface
        logging.debug(request.POST)
        line_channel_membership = request.POST.get('line_channel_membership_id', request.session.get('line_channel_membership_id'))
        if not line_channel_membership:
            messages.warning(request, "your account was missing, order must be restarted")
            return redirect('shop:menu', shop_slug=self.shop.slug)

        order, o_created = Order.objects.get_or_create(line_channel_membership=line_channel_membership, completed_at=None)

        # update_order(order, request.POST)

        return render(request, 'menu.html', self.context)


    def put(self, request, *args, **kwargs): #json interface
        logging.debug(request.PUT)
        order, o_created = Order.objects.get_or_create(line_channel_membership_id=request.session['line_channel_membership_id'], completed_at=None)

        cart_dict = json.loads(request.PUT.get('autosave_data'))
        if not cart_dict or not isinstance(cart_dict, dict):
            return JsonResponse("sorry, I can only take a dict", status=status.HTTP_406_NOT_ACCEPTABLE)

        update_order(order, cart_dict['cart_items'])

        order_cart_dict = order.get_cart_dict()
        return JsonResponse(json.dumps(order_cart_dict), status=status.HTTP_202_ACCEPTED)

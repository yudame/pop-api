import json
import logging

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
from apps.shop.views.order import async_update_order, update_order, OrderException
from apps.shop.views.shop import ShopViewMixin


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
            "shopping_cart_json": json.dumps(order.get_cart_dict()),
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

        shopping_cart = json.loads(request.POST.get('shopping_cart'))
        if isinstance(shopping_cart, dict):
            order.draft_cart = shopping_cart
        else:
            return JsonResponse({'error': "sorry, I can only take a dict"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if request.POST.get('checkout', "false").lower() == "true":
            logging.debug("ready for checkout!")
            async_update_order(order, send_order_summary=True)  # includes saving the order
            return JsonResponse({'success': "order saved"}, status=status.HTTP_202_ACCEPTED)

        else:
            try:
                order = update_order(order)  # includes saving the order
            except OrderException as e:
                return JsonResponse({"error": str(e)}, status=status.HTTP_202_ACCEPTED)

            context = {
                "shopping_cart_json": json.dumps(order.get_cart_dict()),
                "success": "order saved",
            }
            return JsonResponse(context, status=status.HTTP_202_ACCEPTED)

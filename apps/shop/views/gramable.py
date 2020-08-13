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
from apps.shop.models.order import DRAFT, PLACED, CUSTOMER_CANCELLED, SHOP_REJECTED, SHOP_CONFIRMED, SHOP_COMPLETE, EXPIRED
from apps.shop.views.shop import ShopViewMixin
from settings import HOSTNAME


class OrderException(Exception):
    pass


class GramablesView(LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):
    def get(self, request, *args, **kwargs):
        new_gramables = self.shop.gramables.filter(
            item__isnull=True,
            items_as_alt_image__isnull=True,
            shop_as_logo__isnull=True,
            shop_as_icon__isnull=True
        ).order_by('-created_at')

        self.context.update({
            'new_gramables': new_gramables,
            'used_gramables': self.shop.gramables.exclude(
                id__in=[image.id for image in new_gramables]
            )
        })
        return render(request, 'gramables.html', self.context)


# class GramableView(LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):
#
#     def get(self, request, order_id, *args, **kwargs):
#         order = get_object_or_404(Order, id=order_id)
#         # if order not in self.shop.orders.all():
#         #     return HttpResponseNotFound()  # 404
#         self.context['order'] = order
#         return render(request, 'gramable.html', self.context)

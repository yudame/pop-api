from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import View

from apps.common.models import Image
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
            ),
        })
        return render(request, 'gramables.html', self.context)


class GramableView(LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):
    def get(self, request, image_id, *args, **kwargs):
        return redirect('shop:gramables')

    def post(self, request, image_id, *args, **kwargs):
        image = get_object_or_404(Image, id=image_id)
        # if image not in self.shop.gramables.all():
        #     return HttpResponseNotFound()  # 404
        item_id = request.POST.get('item_id', None)
        alt_image = request.POST.get('alt_image', False)

        if item_id:
            item = self.shop.menu.items.filter(id=item_id).first()
            if item and not alt_image:
                item.image_id = image_id
                item.save()
            elif item and alt_image:
                item.alt_images.add(id=image_id)

        return redirect('shop:gramables')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from apps.shop.models import Shop
from apps.shop.views.login_mixins import LineRichMenuLoginMixin, OTPLoginMixin


class ShopViewMixin(View):
    def dispatch(self, request, shop_id=None, shop_slug=None, *args, **kwargs):
        if shop_slug:
            self.shop = get_object_or_404(Shop, slug=shop_slug)
        elif shop_id:
            self.shop = get_object_or_404(Shop, id=shop_id)
        elif request.session.get('shop_id'):
            self.shop = get_object_or_404(Shop, id=request.session['shop_id'])
        elif getattr(request.user, 'shop', None):
            self.shop = request.user.shop
        else:
            return HttpResponseNotFound()  # 404

        request.session['shop_id'] = self.shop.id
        self.context = {
            "shop": self.shop,
        }
        return super().dispatch(request, shop_slug="", *args, **kwargs)


# ShopViewMixin, LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin,
class ShopView(LineRichMenuLoginMixin, OTPLoginMixin, ShopViewMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop.html', self.context)

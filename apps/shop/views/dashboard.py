from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from apps.shop.models import Shop
from apps.shop.views.login_mixins import LineRichMenuLoginMixin, OTPLoginMixin
from apps.shop.views.shop import ShopViewMixin


class DashboardView(LineRichMenuLoginMixin, OTPLoginMixin, LoginRequiredMixin, ShopViewMixin, View):
    def dispatch(self, request, shop_slug="", *args, **kwargs):
        self.context = {
            "shop": self.shop
        }
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', self.context)

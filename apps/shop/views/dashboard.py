from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from apps.shop.models import Shop
from apps.shop.views.setup import ShopOwnerRequiredMixin
from apps.shop.views.shop import ShopViewMixin


class DashboardView(LoginRequiredMixin, ShopViewMixin, ShopOwnerRequiredMixin, View):
    def dispatch(self, request, shop_slug="", *args, **kwargs):
        # anything here will run before mixins
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', self.context)

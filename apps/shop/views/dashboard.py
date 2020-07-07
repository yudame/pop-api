import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseNotFound

from apps.common.views.iommi_prototype import Page, html, Table, Form, Column
from apps.shop.models import Shop, Item


class DashboardView(LoginRequiredMixin, View):
    def dispatch(self, request, shop_slug="", *args, **kwargs):
        if not shop_slug:
            try:
                return redirect('shop:dashboard_with_slug', request.user.shop.get_slug())
            except AttributeError:  # user.shop is missing
                if request.user.is_staff:
                    return redirect('admin:index')
                else:
                    return HttpResponseNotFound()  # 404

        self.shop = get_object_or_404(Shop, slug=shop_slug)
        self.context = {
            "shop": self.shop
        }
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', self.context)

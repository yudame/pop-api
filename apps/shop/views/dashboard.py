from django.contrib.auth import login
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from apps.shop.models import Shop
from apps.user.models import User


class LoginOrOTPMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        username, otp = request.GET.get('username'), request.GET.get('otp')
        if username and otp:
            user_query = User.objects.filter(username=username)
            if user_query.exists():
                user = user_query.first()
                if otp == user.get_otp():
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class DashboardView(LoginOrOTPMixin, View):
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

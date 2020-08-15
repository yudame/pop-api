from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from apps.shop.views.setup_forms import ShopFormA, ShopFormB, ShopFormC, \
    LineChannelFormA, LineChannelFormB, LineChannelFormC, \
    PushoverForm
from apps.shop.views.shop import ShopViewMixin


class ShopOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):  # test run by UserPassesTestMixin

        if self.shop and any([
            self.request.user.is_staff,
            self.request.user == self.shop.owner,
            # self.shop.owner.mentor_users.filter(user_id=self.request.user.id).exists(),
        ]):
            return True
        return False


class SetupView(LoginRequiredMixin, ShopViewMixin, ShopOwnerRequiredMixin, View):
    def dispatch(self, request, shop_id, *args, **kwargs):
        self.shop_setup_forms = [
            ShopFormA, ShopFormB, ShopFormC,
            LineChannelFormA, LineChannelFormB, LineChannelFormC,
            PushoverForm,
        ]
        request.session['shop_setup_form_index'] = request.session.get('shop_setup_form_index', 0)
        self.current_form = self.shop_setup_forms[request.session['shop_setup_form_index']]
        return super().dispatch(request, shop_id, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        if 'LineChannel' in self.current_form.__name__:
            shop_setup_form = self.current_form(instance=self.shop.customer_line_channel)
        else:
            shop_setup_form = self.current_form(instance=self.shop)

        context = {
            'shop': self.shop,
            'shop_setup_form': shop_setup_form
        }
        return render(request, 'setup.html', context)

    def post(self, request, *args, **kwargs):
        shop_setup_form = self.current_form(
            request.POST,
            instance=self.shop.customer_line_channel if 'LineChannel' in self.current_form.__name__ else self.shop
        )

        if shop_setup_form.is_valid():
            shop_setup_form.save()
            if request.POST.get('submit') == 'Back':
                request.session['shop_setup_form_index'] -= 1
            elif request.session.get('shop_setup_form_index', len(self.shop_setup_forms)) < len(self.shop_setup_forms) - 1:
                request.session['shop_setup_form_index'] += 1
            elif self.shop.slug:
                return redirect('shop:dashboard', shop_slug=self.shop.slug)
            else:
                request.session['shop_setup_form_index'] = 0

            return redirect('shop:setup', shop_id=self.shop.id)
        else:
            context = {
                'shop': self.shop,
                'shop_setup_form': shop_setup_form
            }
            return render(request, 'setup.html', context)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from apps.line_app.models import LineChannel
from apps.shop.models import Shop
from apps.shop.views.shop_setup_forms import ShopFormA, ShopFormB, ShopFormC, LineChannelFormA, LineChannelFormB


class SetupView(LoginRequiredMixin, View):
    def dispatch(self, request, shop_id, *args, **kwargs):

        self.shop = get_object_or_404(Shop, id=shop_id)
        if not any([
            request.user.is_staff,
            request.user == self.shop.owner
        ]):
            return self.handle_no_permission()

        if not request.session.get('shop_setup_form_index'):
            request.session['shop_setup_form_index'] = 0

        self.shop_setup_forms = [ShopFormA, ShopFormB, ShopFormC, LineChannelFormA, LineChannelFormB]
        self.current_form = self.shop_setup_forms[request.session.get('shop_setup_form_index', 0)]

        return super().dispatch(request, *args, **kwargs)

    def get_form_class_instance(self):
        if self.current_form.Meta.model == Shop:
            return self.shop
        elif self.current_form.Meta.model == LineChannel:
            line_channel, lc_created = LineChannel.objects.get_or_create(shop=self.shop)
            return line_channel

    def get(self, request, *args, **kwargs):
        context = {
            'shop': self.shop,
            'shop_setup_form': self.current_form(instance=self.get_form_class_instance())
        }
        return render(request, 'setup.html', context)

    def post(self, request, *args, **kwargs):
        shop_setup_form = self.current_form(request.POST, instance=self.get_form_class_instance())

        if shop_setup_form.is_valid():
            shop_setup_form.save()
            if request.POST.get('submit') == 'Back':
                request.session['shop_setup_form_index'] -= 1
            elif request.session.get('shop_setup_form_index') < len(self.shop_setup_forms) - 1:
                request.session['shop_setup_form_index'] += 1
            else:
                request.session['shop_setup_form_index'] = 0

            return redirect('shop:setup', shop_id=self.shop.id)
        else:
            context = {
                'shop': self.shop,
                'shop_setup_form': shop_setup_form
            }
            return render(request, 'setup.html', context)

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.utils.translation import gettext_lazy as _
from fontawesome_5 import Icon

from apps.shop.models import Shop


class BootstrapModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())
        for field_name, field in self.fields.items():
            # add form-control class to all fields
            field.widget.attrs['class'] = 'form-control'
            # set default textarea size to just 4 rows
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 4
            # set icon attr on field object
            if field_name in icons:
                field.icon = icons[field_name]


class ShopFormA(BootstrapModelForm):
    class Meta:
        model = Shop
        fields = [
            'name', 'description', 'unstructured_text_address',
        ]
        labels = {
            'name': _('Name'), 'description': _('About'), 'unstructured_text_address': _('Full Address')
        }
        icons = {
            'name': Icon('store'),
        }
        required_fields = ['name',]

class ShopFormB(BootstrapModelForm):
    class Meta:
        model = Shop
        fields = [
            'facebook_href', 'instagram_href', 'google_maps_href',
        ]
        labels = {
            'facebook_href': _('Facebook Profile Link'), 'instagram_href': _('Instagram Profile Link'), 'google_maps_href': _('Google Maps Profile Link')
        }
        icons = {
            'facebook_href': Icon('facebook', 'fab'), 'instagram_href': Icon('instagram', 'fab'), 'google_maps_href': Icon('map-marker'),
        }


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

        self.shop_setup_forms = [ShopFormA, ShopFormB]
        self.current_form = self.shop_setup_forms[request.session.get('shop_setup_form_index', 0)]

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'shop': self.shop,
            'shop_setup_form': self.current_form(instance=self.shop)
        }
        return render(request, 'setup.html', context)

    def post(self, request, *args, **kwargs):
        shop_setup_form = self.current_form(request.POST, instance=self.shop)

        if shop_setup_form.is_valid():
            shop_setup_form.save()
            if request.session.get('shop_setup_form_index') < len(self.shop_setup_forms) - 1:
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

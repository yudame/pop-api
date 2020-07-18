
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from fontawesome_5 import Icon

from apps.line_app.models import LineChannel
from apps.shop.models import Shop
from settings import HOSTNAME


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
            'name', 'description', 'base_language'
        ]
        labels = {
            'name': _('Name'), 'description': _('About'), 'base_language': _('First Language')
        }
        icons = {
            'name': Icon('store'),
        }
        required_fields = ['name',]

class ShopFormB(BootstrapModelForm):
    class Meta:
        model = Shop
        fields = [
            'unstructured_text_address', 'contact_name', 'contact_phone_number', 'contact_email',
        ]
        labels = {
            'unstructured_text_address': _('Full Address'),
        }


class ShopFormC(BootstrapModelForm):
    class Meta:
        model = Shop
        fields = [
            'slug', 'facebook_href', 'instagram_href', 'google_maps_href', 'trip_advisor_href'
        ]
        labels = {
            'slug': _('Pop Handle'),
            'facebook_href': _('Facebook Profile Link'),
            'instagram_href': _('Instagram Profile Link'),
            'google_maps_href': _('Google Maps Profile Link'),
            'trip_advisor_href': _('TripAdvisor Profile Link'),
        }
        icons = {
            'slug': Icon('at'),
            'facebook_href': Icon('facebook', 'fab'),
            'instagram_href': Icon('instagram', 'fab'),
            'google_maps_href': Icon('map-marker'),
            'trip_advisor_href': Icon('tripadvisor', 'fab')
        }

class LineChannelFormA(BootstrapModelForm):
    class Meta:
        model = LineChannel
        fields = [
            'numeric_id', 'name', 'description', 'email_address', 'secret', 'assertion_signing_key', 'creator_user_id',
        ]
        labels = {
            'numeric_id': _('Channel ID'),
            'name': _('Channel name'),
            'description': _('Channel description'),
            'email_address': _('Email address'),
            'secret': _('Channel secret'),
            'assertion_signing_key': _('Assertion Signing Key'),
            'creator_user_id': _('Your user ID'),
        }

class LineChannelFormB(BootstrapModelForm):

    line_bot_callback_uri = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}))
    use_webhook = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    allow_groups = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    auto_reply = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    greeting = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    access_token = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs['initial'] = {
                'line_bot_callback_uri': f"https://{HOSTNAME}{instance.line_bot_callback_uri}",
                'use_webhook': _("ON"),
                'allow_groups': _("Disabled"),
                'auto_reply': _("Disabled"),
                'greeting': _("Disabled"),
            }
        return super().__init__(*args, **kwargs)

    class Meta:
        model = LineChannel
        fields = [
            'bot_id', 'line_bot_callback_uri', 'use_webhook', 'allow_groups', 'auto_reply', 'greeting', 'access_token',
        ]
        labels = {
            'bot_id': _('Bot basic ID'),
            'line_bot_callback_uri': _('Webhook URL'),
            'use_webhook': _('Use webhook'),
            'allow_groups': _('Allow bot to join group chats'),
            'auto_reply': _('Auto-reply messages'),
            'greeting': _('Greeting messages'),
            'access_token': _('Channel access token (long-lived)'),
        }
        readonly_fields = ('line_bot_callback_uri', 'use_webhook')


class LineChannelFormC(BootstrapModelForm):
    class Meta:
        model = LineChannel
        fields = ['direct_link_url',]
        labels = {
            'direct_link_url': _('Direct link'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance and instance.bot_id:
            self.fields['direct_link_url'].help_text += f'''
                <br/>
                can be found at
                <i class="fas fa-link"></i> 
                <a href="{instance.account_manager_url}/gainfriends" style="text-decoration: underline;cursor: pointer;" target="_blank">
                    LINE Account Manager - Gain Friends
                </a>.
            '''

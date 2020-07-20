import logging
import uuid
from django.db import models
from django.urls import reverse
from django.utils.http import urlencode
from linebot.models import TextMessage, LocationMessage, ImageMessage, StickerMessage
from pinax.referrals.models import Referral

from apps.common.models import Image
from apps.line_app.views.delivery import Delivery
from apps.line_app.views.line_bot import LineBot
from apps.common.behaviors import Timestampable
from apps.line_app.views.menu import Menu
from settings import HOSTNAME


(CUSTOMER_CHANNEL, ADMIN_CHANNEL, LOGIN_CHANNEL) = ('bot', 'admin', 'login')
CHANNEL_TYPE_CHOICES = [
    (CUSTOMER_CHANNEL, 'customer messaging API'),
    (ADMIN_CHANNEL, 'admin messaging API'),
    (LOGIN_CHANNEL, 'LINE Login'),
]

class LineChannel(Timestampable, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    shop = models.ForeignKey('shop.Shop', null=True, on_delete=models.PROTECT, related_name="line_channel")
    channel_type = models.CharField(max_length=5, choices=CHANNEL_TYPE_CHOICES, null=False)

    name = models.CharField(max_length=31)
    description = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    privacy_policy_url = models.URLField(null=True, blank=True)
    terms_url = models.URLField(null=True, blank=True)

    numeric_id = models.CharField(max_length=10, null=True, blank=True,
                                  help_text="Channel ID at top of basic settings screen")
    secret = models.CharField(max_length=32, null=True, blank=True,
                              help_text="Channel secret on basic settings screen")
    assertion_signing_key = models.CharField(max_length=40, null=True, blank=True)
    bot_id = models.CharField(max_length=31, null=True, blank=True, help_text="eg. @A1b2c3")
    direct_link_url = models.URLField(null=True, blank=True, help_text="eg. https://lin.ee/123abc")

    access_token = models.CharField(max_length=200, null=True, blank=True)

    creator_user_id = models.CharField(max_length=40, null=True, blank=True)

    # MODEL PROPERTIES
    @property
    def line_bot_callback_uri(self):
        return reverse('line_app:callback', kwargs={'line_channel_id': self.id})

    @property
    def QR_img_src(self):
        if self.bot_id:
            return f"https://qr-official.line.me/sid/M/{self.bot_id.strip('@')}.png"
        return ""

    @property
    def line_share_url(self):
        if self.bot_id:
            return f"https://line.me/R/nv/recommendOA/{self.bot_id}"
        return ""

    @property
    def account_manager_url(self):
        if self.bot_id:
            return f"https://manager.line.biz/account/{self.bot_id}"
        return ""

    # MODEL FUNCTIONS
    def get_bot(self):
        if not hasattr(self, 'line_bot'):
            self.line_bot = LineBot(self)
        return self.line_bot

    def respond_to(self, line_event):
        from apps.line_app.models import LineUserProfile
        line_user_profile = LineUserProfile.objects.get(line_user_id=line_event.source.user_id)
        user = line_user_profile.user

        if isinstance(line_event.message, TextMessage):
            if line_event.message.text == "menu":
                menu = Menu()
                return menu.render_bot_message()
                # return MenuMessage
            elif line_event.message.text == "share":
                return self.line_share_url
            elif line_event.message.text == "refer":
                referral = Referral.objects.get_or_create(
                    user=user,
                    label="general",
                    redirect_to=self.line_share_url
                )
                return referral.url
            elif line_event.message.text == "delivery":
                delivery = Delivery()
            elif line_event.message.text == "dashboard":
                # get link to shop dasbhoard and include otp login credentials
                if user.is_staff or self.shop == user.shop:  # owner of shop
                    login_kwargs = {'username': user.username, 'otp': user.get_otp()}
                    return f"Manage {self.shop.name} at " + f'https://{HOSTNAME}{self.shop.get_absolute_url()}?{urlencode(login_kwargs)}'
                else:
                    return "sorry admins only 🤨"

            else:
                return "received " + line_event.message.text
        elif isinstance(line_event.message, ImageMessage):

            logging.debug(line_event.message.content_provider.original_content_url,
                          line_event.message.content_provider.preview_image_url)

            message_content = self.line_bot.api.get_message_content(line_event.message.id)
            filename = '/tmp/some_image.unknown'
            with open(filename, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)

            empty_grammables = self.shop.gramables.filter(url="", original_url="")
            if empty_grammables.exists():
                image = empty_grammables.first()
            else:
                image = Image.objects.create()
                self.shop.gramables.add(image)

            image.upload_file(filename)
            image.save()

            if image.original_url:
                return "✓ photo saved"
            else:
                return "problem, Line didn't provide a url. I just got this: " + str(line_event.message.content_provider.__dict__)

        elif isinstance(line_event.message, LocationMessage):
            line_user_profile = LineUserProfile.objects.get(line_user_id=line_event.source.user_id)
            line_user_profile.save_location(line_event.message)
            return "Thanks! your location is saved 📍"
        else:
            return "🆗👍"

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('shop', 'channel_type')

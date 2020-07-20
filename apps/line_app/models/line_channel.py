import logging
import uuid
from django.db import models
from django.urls import reverse

from apps.common.behaviors import Timestampable


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

    @property
    def welcome_text(self):
        return "Hi 👋 Now you can get rewards✹ and click the menu button to order."

    # MODEL FUNCTIONS
    def get_bot(self):
        if not hasattr(self, 'line_bot'):
            from apps.line_app.views.line_bot import LineBot
            self.line_bot = LineBot(self)
        return self.line_bot


    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('shop', 'channel_type')

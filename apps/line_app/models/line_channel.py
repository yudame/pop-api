import logging
import uuid
from django.db import models
from django.urls import reverse
from linebot.models import TextMessage, LocationMessage, ImageMessage, StickerMessage

from apps.line_app.views.delivery import Delivery
from apps.line_app.views.line_bot import LineBot
from apps.common.behaviors import Timestampable


class LineChannel(Timestampable, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=31)
    description = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    privacy_policy_url = models.URLField(null=True, blank=True)
    terms_url = models.URLField(null=True, blank=True)

    numeric_id = models.CharField(max_length=10, null=True, blank=True)
    secret = models.CharField(max_length=32, null=True, blank=True)
    assertion_signing_key = models.CharField(max_length=40, null=True, blank=True)
    bot_id = models.CharField(max_length=31, null=True, blank=True)
    access_token = models.CharField(max_length=200, null=True, blank=True)

    creator_user_id = models.CharField(max_length=40, null=True, blank=True)

    # MODEL PROPERTIES
    @property
    def line_bot_callback_uri(self):
        return reverse('line_app:callback', kwargs={'line_channel_id': self.id})


    # MODEL FUNCTIONS
    def get_bot(self):
        if not hasattr(self, 'line_bot'):
            self.line_bot = LineBot(self)
        return self.line_bot

    def respond_to(self, line_event):
        from apps.line_app.models import LineUserProfile

        if isinstance(line_event.message, TextMessage):
            if line_event.message.text == "menu":
                return 'menu coming soon'
                # return MenuMessage
            elif line_event.message.text == "delivery":
                return Delivery.render_bot_message()
            return line_event.message.text
        elif isinstance(line_event.message, LocationMessage):
            line_user_profile = LineUserProfile.objects.get(line_user_id=line_event.source.user_id)
            line_user_profile.save_location(line_event.message)
            return "Thanks! your location is saved"
        else:
            return "Ok, roger.."

    def __str__(self):
        return self.name

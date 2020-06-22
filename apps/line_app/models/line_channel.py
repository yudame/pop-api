import uuid
from django.db import models
from django.urls import reverse
from linebot.models import TextMessage

from apps.common.behaviors import Timestampable
from apps.line_app.views.line_bot import LineBot


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
        return LineBot(self)

    def respond_to(self, message_type, line_event):
        if message_type == TextMessage:
            return line_event.message.text
        return "Ok, roger.."

    def __str__(self):
        return self.name

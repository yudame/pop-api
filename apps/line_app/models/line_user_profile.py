from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from linebot.models import LocationMessage

from apps.common.behaviors import Timestampable
from apps.user.models import User
from settings import AUTH_USER_MODEL


class LineUserProfile(Timestampable, models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)

    line_user_id = models.CharField(max_length=40)
    name = models.CharField(max_length=30, null=True)
    language = models.CharField(max_length=8, null=True)
    picture_url = models.URLField(null=True)
    status_message = models.CharField(max_length=550, null=True)

    line_channels = models.ManyToManyField('line_app.LineChannel', through='line_app.LineChannelMembership', blank=True)

    line_username_id = models.CharField(max_length=25, null=True)  # public line username, optional

    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def check_has_user(self):
        if self.user:
            return True
        self.user = User.objects.create()
        self.save()

    def say_my_name(self):
        for line_channel in self.line_channels.all():
            line_bot = line_channel.get_bot()
            line_bot.send_text_message(self, f"{_('AFAIK, your name is')} {self.name or '_?_'}.")

    def show_my_face(self):
        if self.picture_url:
            for line_channel in self.line_channels.all():
                line_bot = line_channel.get_bot()
                line_bot.send_image_message(self, self.picture_url)

    def save_location(self, line_location_message):
        if not isinstance(line_location_message, LocationMessage):
            return False

        self.check_has_user()

        self.user.unstructured_text_address = ""
        if line_location_message.title:
            self.user.unstructured_text_address = f"{line_location_message.title}: "
        self.user.unstructured_text_address += f"{line_location_message.address}"
        self.user.latitude = line_location_message.latitude
        self.user.longitude = line_location_message.longitude
        self.user.save()
        return True

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common.behaviors import Timestampable


class LineUserProfile(Timestampable, models.Model):

    # user = models.OneToOneField(User, on_delete=models.CASCADE) #OneToOneField is used to extend the original User object provided from Django.

    user_id = models.CharField(max_length=40)

    name = models.CharField(max_length=30, null=True)
    language = models.CharField(max_length=8, null=True)
    picture_url = models.URLField(null=True)
    status_message = models.CharField(max_length=550, null=True)

    line_channels = models.ManyToManyField('line_app.LineChannel', through='line_app.LineChannelMembership', blank=True)

    line_id = models.CharField(max_length=25, null=True)  # public line username, optional

    # MODEL PROPERTIES

    # MODEL FUNCTIONS

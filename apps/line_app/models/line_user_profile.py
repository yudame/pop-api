from django.db import models

from apps.common.behaviors import Timestampable


class LineUserProfile(Timestampable, models.Model):

    # user = models.OneToOneField(User, on_delete=models.CASCADE) #OneToOneField is used to extend the original User object provided from Django.

    line_id = models.CharField(max_length=50)
    name = models.CharField(max_length=30, null=True)
    language = models.CharField(max_length=8, null=True)
    picture_url = models.URLField(null=True)
    status_message = models.CharField(max_length=550, null=True)

    line_channels = models.ManyToManyField('line_app.LineChannel', through='line_app.LineChannelMembership', blank=True)

    # MODEL PROPERTIES

    # MODEL FUNCTIONS

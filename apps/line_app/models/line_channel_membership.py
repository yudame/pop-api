from django.db import models
from apps.common.behaviors import Timestampable


class LineChannelMembership(Timestampable, models.Model):
    line_user_profile = models.ForeignKey('line_app.LineUserProfile', on_delete=models.CASCADE,
                                          related_name='line_channel_memberships')
    line_channel = models.ForeignKey('line_app.LineChannel', on_delete=models.CASCADE,
                                     related_name='line_channel_memberships')

    is_following = models.BooleanField(default=False)
    is_promotable = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text='user is admin or staff for line channel')

    # MODEL PROPERTIES

    @property
    def uuid(self):
        return f"{self.line_channel.id}:{self.line_user_profile.line_user_id}"


    # MODEL FUNCTIONS

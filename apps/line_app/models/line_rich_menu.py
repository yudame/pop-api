import logging
import os

import requests
from linebot.models import RichMenu, RichMenuBounds, RichMenuArea, URIAction, PostbackAction, RichMenuSize
from django.db import models

from settings import STATICFILES_DIRS, HOSTNAME


class LineRichMenu(models.Model):
    line_channel = models.ForeignKey('line_app.LineChannel', on_delete=models.CASCADE, related_name='line_rich_menus')
    index = models.IntegerField(default=1)
    # admin_only = models.BooleanField(default=False)
    line_rich_menu_id = models.CharField(max_length=50, null=True)

    # MODEL PROPERTIES
    @property
    def rich_menu_object(self):
        return RichMenu(
            size=RichMenuSize(width=1000, height=315),
            selected=True,
            name="Menu",
            chat_bar_text="Start",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=15, y=8, width=300, height=300),
                    action=PostbackAction(label='Call', data='action=place_call')
                    # action=URIAction(label='Call', uri=f'tel:{self.line_channel.shop.contact_phone_number}')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=300+33+15, y=8, width=300, height=300),
                    action=PostbackAction(label='Order', data='action=get_menu')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=600 + 67 + 15, y=8, width=300, height=300),
                    action=URIAction(label='Preferences', uri=f'https://{HOSTNAME}{self.line_channel.shop.get_absolute_url()}')
                ),
            ]
        )

    # MODEL FUNCTIONS

    def publish(self):
        line_channel_bot = self.line_channel.get_bot()
        self.line_rich_menu_id = line_channel_bot.api.create_rich_menu(rich_menu=self.rich_menu_object)

        logging.debug("rich_menu_id", self.line_rich_menu_id)

        # upload image and link it to richmenu
        # from https://developers.line.biz/en/reference/messaging-api/#upload-rich-menu-image
        with open(os.path.join(STATICFILES_DIRS[0], 'image/menu-circle-buttons.png'), 'rb') as f:
            line_channel_bot.api.set_rich_menu_image(self.line_rich_menu_id, 'image/png', f)

        self.save()
        return self.line_rich_menu_id


    def assign_to_user(self, user_object):
        line_channel_bot = self.line_channel.get_bot()
        if not self.line_rich_menu_id:
            self.publish()
        line_channel_bot.api.link_rich_menu_to_user(
            user_object.line_user_profile.line_user_id,
            self.line_rich_menu_id
        )


    def assign_to_users(self, user_queryset):
        line_channel_bot = self.line_channel.get_bot()
        if not self.line_rich_menu_id:
            self.publish()

        line_channel_bot.api.link_rich_menu_to_users(
            [user.line_user_profile.line_user_id for user in user_queryset],
            self.line_rich_menu_id
        )


import requests
from linebot.models import RichMenu, RichMenuBounds, RichMenuArea, URIAction, PostbackAction
from django.db import models


class LineRichMenu(models.Model):

    line_channel = models.ForeignKey('line_app.LineChannel', on_delete=models.CASCADE, related_name='line_rich_menus')
    index = models.IntegerField(default=1)

    # MODEL PROPERTIES

    # MODEL FUNCTIONS

    def publish(self):
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=800, height=540),  # 2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="NextPage",
            chat_bar_text="See Menu",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=400, height=540),
                    action=URIAction(label='Thinktron', uri='https://www.thinktronltd.com/')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=400, y=0, width=400, height=540),
                    action=PostbackAction(label='Next Page', data='action=nextpage')),
            ]
        )

        line_bot = self.line_channel.get_bot()

        rich_menu_id = line_bot.api.create_rich_menu(rich_menu=rich_menu_to_create)
        print("rich_menu_id", rich_menu_id)

        # upload image and link it to richmenu
        # from https://developers.line.biz/en/reference/messaging-api/#upload-rich-menu-image
        with open(os.path.join('images', 'firstpage.jpg'), 'rb') as f:
            line_bot.api.set_rich_menu_image(rich_menu_id, 'image/jpeg', f)  # set as default image

        url = "https://api.line.me/v2/bot/user/all/richmenu/" + rich_menu_id
        requests.post(url, headers={"Authorization": "Bearer " + self.line_channel.access_token})

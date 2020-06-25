import json
import logging
from abc import ABC
from datetime import timedelta

from django.utils import timezone
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, SendMessage, ImageMessage, StickerMessage, \
    FileMessage, LocationMessage, ImageSendMessage
from linebot.models import SourceUser
from apps.common.utilities.multithreading import start_new_thread


class LineBot(ABC):

    def __init__(self, line_channel):

        self.line_channel = line_channel
        self.api = LineBotApi(line_channel.access_token)
        try:
            self.shop = line_channel.shop
        except:  # todo: put proper exception type here
            self.shop = None

        self._setup_handler()

    @start_new_thread
    def handle(self, request_data_string, signature):
        logging.debug("Request body: " + request_data_string)

        # request_data_dict = json.loads(request_data_string)

        payload = self.handler.parser.parse(request_data_string, signature, as_payload=True)
        for event in payload.events:
            if isinstance(event.source, SourceUser):
                self.follower_registration(str(event.source.user_id))

        self.handler.handle(request_data_string, signature)
        from django.db import connection
        connection.close()

    def _setup_handler(self):
        self.handler = WebhookHandler(self.line_channel.secret)

        for message_type in (TextMessage, ImageMessage, StickerMessage, FileMessage, LocationMessage):

            @self.handler.add(MessageEvent, message=message_type)
            def handle_message(event):
                response = self.line_channel.respond_to(message_type, event)
                if isinstance(response, str):
                    self.api.reply_message(event.reply_token, TextSendMessage(text=response))
                elif isinstance(response, SendMessage):
                    self.api.reply_message(event.reply_token, response)
                else:
                    raise Exception("response is not of type SendMessage from linebot.models")

        @self.handler.default()
        def default_handler(event):
            self.api.reply_message(event.reply_token, TextSendMessage(text="well.. that was unexpected"))

    def follower_registration(self, follower_user_id: str, force_update: bool = False) -> None:
        """
        check user is in profile database and has line channnel membership
        :param follower_user_id: string eg. "U1a195ed7fa0fc615589f3105ec9d0a95"
        :return: None
        """
        # if not all([
        #     len(follower_user_id) > 4,
        #     follower_user_id.startswith('U')
        # ]):
        #     return
        from apps.line_app.models import LineUserProfile, LineChannelMembership
        line_user_profile, lup_created = LineUserProfile.objects.get_or_create(user_id=follower_user_id)
        LineChannelMembership.objects.get_or_create(line_user_profile=line_user_profile,
                                                    line_channel=self.line_channel)
        try:
            if any([
                lup_created,
                force_update,
                not line_user_profile.name,
                line_user_profile.modified_at > timezone.now() - timedelta(days=28)
            ]):
                line_profile = self.api.get_profile(follower_user_id)
                line_user_profile.name = line_profile.display_name
                line_user_profile.picture_url = line_profile.picture_url
                line_user_profile.language = line_profile.language
                line_user_profile.status_message = line_profile.status_message
                line_user_profile.save()
        except Exception as e:
            logging.warning(str(e))


    def send_text_message(self, to_user_profile, text):
        self.api.push_message(to_user_profile.user_id, TextSendMessage(text=text))

    def send_image_message(self, to_user_profile, image_url, thumbnail_image_url=None):
        thumbnail_image_url = thumbnail_image_url or image_url
        self.api.push_message(to_user_profile.user_id, ImageSendMessage(image_url, thumbnail_image_url))

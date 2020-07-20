import logging
from abc import ABC
from datetime import timedelta

from django.utils import timezone
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, SendMessage, ImageMessage, StickerMessage, \
    FileMessage, LocationMessage, ImageSendMessage, FollowEvent
from linebot.models import SourceUser

from apps.common.utilities.multithreading import start_new_thread
from apps.line_app.models import LineUserProfile, LineChannelMembership


class LineBot(ABC):

    def __init__(self, line_channel):
        self.line_channel = line_channel
        self.api = LineBotApi(line_channel.access_token)
        self._setup_handler()

    @start_new_thread
    def handle(self, request_data_string, signature):
        logging.debug("Request body: " + request_data_string)

        # request_data_dict = json.loads(request_data_string)

        payload = self.handler.parser.parse(request_data_string, signature, as_payload=True)
        last_user_id = None
        for event in payload.events:
            if isinstance(event.source, SourceUser):
                if last_user_id != str(event.source.user_id):
                    self.follower_registration(str(event.source.user_id))
                    last_user_id = str(event.source.user_id)

        self.handler.handle(request_data_string, signature)
        from django.db import connection
        connection.close()

    def _setup_handler(self):
        self.handler = WebhookHandler(self.line_channel.secret)

        for message_type_class in [FileMessage, LocationMessage, StickerMessage, ImageMessage, TextMessage, ]:

            @self.handler.add(MessageEvent, message=message_type_class)
            def handle_message(event):
                response = LineChannelMembership.objects.get(
                    line_user_profile__line_user_id=str(event.source.user_id),
                    line_channel=self.line_channel
                ).respond_to(event)
                if isinstance(response, str):
                    self.api.reply_message(event.reply_token, TextSendMessage(text=response))
                elif isinstance(response, SendMessage):
                    self.api.reply_message(event.reply_token, response)
                else:
                    raise Exception("response is not of type SendMessage from linebot.models")

        @self.handler.add(FollowEvent)
        def default_handler(event):
            LineChannelMembership.objects.get(
                line_user_profile__line_user_id=str(event.source.user_id),
                line_channel=self.line_channel
            ).set_rich_menu()
            self.api.reply_message(event.reply_token, TextSendMessage(text=self.line_channel.welcome_text))

        @self.handler.default()
        def default_handler(event):
            self.api.reply_message(event.reply_token, TextSendMessage(text="well.. that was unexpected"))

    def follower_registration(self, follower_line_user_id: str, force_update: bool = False) -> None:
        """
        check user is in profile database and has line channel membership
        :param follower_line_user_id: string eg. "U1a195ed7fa0fc615589f3105ec9d0a95"
        :return: None
        """
        # if not all([
        #     len(follower_line_user_id) > 4,
        #     follower_line_user_id.startswith('U')
        # ]):
        #     return

        line_user_profile, lup_created = LineUserProfile.objects.get_or_create(line_user_id=follower_line_user_id)
        LineChannelMembership.objects.get_or_create(line_user_profile=line_user_profile,
                                                    line_channel=self.line_channel)
        try:
            if any([
                lup_created,
                force_update,
                line_user_profile.modified_at < timezone.now() - timedelta(days=2)
            ]):
                line_profile = self.api.get_profile(follower_line_user_id)
                line_user_profile.name = line_profile.display_name
                line_user_profile.picture_url = line_profile.picture_url
                line_user_profile.language = line_profile.language
                line_user_profile.status_message = line_profile.status_message
                line_user_profile.save()
        except Exception as e:
            logging.warning(str(e))


    def send_text_message(self, to_user_profile, text):
        self.api.push_message(to_user_profile.line_user_id, TextSendMessage(text=text))

    def send_image_message(self, to_user_profile, image_url, thumbnail_image_url=None):
        thumbnail_image_url = thumbnail_image_url or image_url
        self.api.push_message(to_user_profile.line_user_id, ImageSendMessage(image_url, thumbnail_image_url))

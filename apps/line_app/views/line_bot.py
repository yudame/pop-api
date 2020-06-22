from abc import ABC
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, SendMessage, ImageMessage, StickerMessage, FileMessage, LocationMessage

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
    def handle(self, request_data, signature):
        self.handler.handle(request_data, signature)
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

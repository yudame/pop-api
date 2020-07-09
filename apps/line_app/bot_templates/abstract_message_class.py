import json
from abc import ABC
from linebot.models import FlexSendMessage, SendMessage, TextSendMessage


class AbstractLineMessage(ABC):

    def __init__(self, object_instance):
        self.object_instance = object_instance

    def render(self) -> SendMessage:
        alt_text = self.render_alt_text(self.object_instance)
        flex_dict = self.render_flex_dict(self.object_instance)

        if flex_dict:
            return FlexSendMessage(
                alt_text=alt_text,
                contents=flex_dict
            )
        elif alt_text:
            return TextSendMessage(alt_text)
        else:
            return TextSendMessage("response not available")

    def render_alt_text(self, object_instance) -> str:
        """
        overwrite me
        :param object_instance:
        :return:
        """
        return ""

    def render_flex_dict(self, object_instance) -> dict:
        """
        overwrite me
        :param object_instance:
        :return:
        """
        return {}

    class Meta:
        abstract = True

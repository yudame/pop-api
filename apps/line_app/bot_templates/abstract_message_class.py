import json
from abc import ABC
from linebot.models import FlexSendMessage, SendMessage, TextSendMessage


class AbstractLineMessage(ABC):

    required_kwargs = []

    def __init__(self, context: dict):
        for kw in self.required_kwargs:
            if kw not in context:
                raise Exception(f"{kw} is missing from context")
        self.context = context

    def render(self, message: str="") -> SendMessage:

        if message:
            return TextSendMessage(message)

        alt_text = self.render_alt_text()
        flex_dict = self.render_flex_dict()

        if flex_dict:
            return FlexSendMessage(
                alt_text=alt_text,
                contents=flex_dict
            )
        elif alt_text:
            return TextSendMessage(alt_text)
        else:
            raise NotImplemented("must provide message or message rendering")

    def render_alt_text(self) -> str:
        """
        overwrite me
        :param object_instance:
        :return:
        """
        raise NotImplementedError("must overwrite render_alt_text method")

    def render_flex_dict(self) -> dict:
        """
        overwrite me
        :param object_instance:
        :return:
        """
        # raise NotImplementedError("must overwrite render_flex_dict method")
        pass

    class Meta:
        abstract = True

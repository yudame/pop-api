from apps.line_app.bot_templates.abstract_message_class import AbstractLineMessage


class ExampleMessage(AbstractLineMessage):

    context_required = [

    ]

    def render_alt_text(self) -> str:
        return "Message for you, sir."

    def render_flex_dict(self) -> dict:
        return {}

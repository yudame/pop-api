from apps.line_app.bot_templates.abstract_message_class import AbstractLineMessage


class ExampleMessage(AbstractLineMessage):

    def render(self, some_instance):
        return {
            'instance': str(some_instance)
        }

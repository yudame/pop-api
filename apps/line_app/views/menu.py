from abc import ABC


class Menu(ABC):

    def render_bot_message(self):
        from apps.shop.models import Shop
        self.shop = Shop.objects.first()

        from apps.line_app.bot_templates.menu import MenuTimelineMessage
        context = {
            'shop': self.shop,
        }
        return MenuTimelineMessage(context).render()

from abc import ABC


class Delivery(ABC):

    def render_bot_message(self):
        from apps.shop.models import Shop
        self.shop = Shop.objects.first()

        from apps.line_app.bot_templates.delivery import DeliveryTimelineMessage
        return DeliveryTimelineMessage(self).render()

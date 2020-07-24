from abc import ABC

from apps.shop.models import Order


class OrderSummary(ABC):

    def __init__(self, order: Order):
        self.order = order
        self.shop = order.line_channel_membership.line_channel.shop

    def render_bot_message(self):
        context = {
            'shop': self.shop,
            'order': self.order
        }
        from apps.line_app.bot_templates.order_summary import OrderSummaryMessage
        return OrderSummaryMessage(context).render()

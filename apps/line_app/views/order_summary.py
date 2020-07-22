from abc import ABC

from apps.shop.models import Order


class OrderSummary(ABC):

    def __init__(self, order: Order):
        self.order = order
        self.shop_name = order_summary_instance.order.line_channel_membership.line_channel.shop.name

    def render_bot_message(self):
        from apps.shop.models import Shop
        self.shop = Shop.objects.first()

        context = {

        }

        from apps.line_app.bot_templates.order_summary import OrderSummaryMessage
        return OrderSummaryMessage(context).render()

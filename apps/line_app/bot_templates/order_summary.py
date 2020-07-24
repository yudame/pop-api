from apps.line_app.bot_templates.abstract_message_class import AbstractLineMessage


class OrderSummaryMessage(AbstractLineMessage):

    context_required = [
        'shop',
        'order',
    ]

    def render_alt_text(self) -> str:
        return "ready to pay"

    def render_flex_dict(self) -> dict:

        order_item_rows = [{
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": (f"{order_item.quantity:.0f}x  " if order_item.quantity > 1 else "") + f"{order_item.item.name}",
                "size": "sm",
                "color": "#202020",
                "flex": 0
              },
              {
                "type": "text",
                "text": f"{order_item.price.amount:.0f}",
                "size": "xs",
                "color": "#707070",
                "align": "end"
              }
            ]
          } for order_item in self.context['order'].order_items.all()]

        return {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "pending order",
        "weight": "bold",
        "color": "#1DB446",
        "size": "sm",
        "style": "italic"
      },
      {
        "type": "text",
        "text": f"{self.context['shop'].name}",
        "weight": "bold",
        "size": "lg",
        "margin": "md"
      },
      {
        "type": "text",
        "text": f"{self.context['shop'].address}",
        "size": "xs",
        "color": "#aaaaaa",
        "wrap": True
      },
      {
        "type": "separator",
        "margin": "lg",
        "color": "#f0f0f0"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "md",
        "spacing": "sm",
        "contents": order_item_rows
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "separator",
            "margin": "sm",
            "color": "#f0f0f0"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "TOTAL",
                "size": "sm",
                "color": "#202020"
              },
              {
                "type": "text",
                "text": f"{self.context['order'].items_total_price.currency} {self.context['order'].items_total_price.amount:.0f}",
                "size": "sm",
                "color": "#707070",
                "align": "end"
              }
            ],
            "spacing": "none",
            "margin": "sm"
          }
        ],
        "margin": "sm"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "margin": "xxl",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "Place Order",
              "data": f"{self.context['order'].id}"
            },
            "style": "primary"
          }
        ]
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}

import logging
from abc import ABC
from apps.common.utilities.multithreading import start_new_thread

from pushover import init, Client
from settings import PUSHOVER_API_TOKEN, PUSHOVER_USER_KEY

init(PUSHOVER_API_TOKEN)


class Pushover(ABC):

    def __init__(self, pushover_user_key=PUSHOVER_USER_KEY, pushover_device_name=""):
        self.client = Client(user_key=pushover_user_key, device=pushover_device_name)

    @start_new_thread
    def send_text(self, text_message: str, title: str="Pop"):
        logging.debug(f"sending text: {text_message}")
        self.client.send_message(text_message, title=title)

    def send_urgent_order(self, order, confirm_order_url, view_order_url):
        message = "\r\n".join([
            f"Order for {order.line_channel_membership.line_user_profile.name} (order #{order.id})",
            " ",
        ])

        for order_item in order.order_items.filter(quantity__gt=0):
            message += "\r\n".join([
                " ",
                f"Item: {order_item.item.name}"
                f"Qty: {order_item.quantity}" 
                f"Note: {order_item.notes.first().text if order_item.notes.exists() else ''}"
            ])

        message += "\r\n".join([
            f"""<a href="{confirm_order_url}">CONFIRM NOW :)</a>""",
            " ",
            f"""<a href="{view_order_url}">VIEW ORDER</a>"""
        ])

        self.client.send_message(
            message=message, html=1,
            title=f"NEW ORDER {order.id}",
            url=confirm_order_url,
            url_title="Confirm Order",
            sound="persistent",
            priority=2, retry=30, expire=(30*4)+25,
        )

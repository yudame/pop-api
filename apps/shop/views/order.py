from decimal import Decimal

from apps.common.utilities.multithreading import start_new_thread
from apps.line_app.models import LineChannelMembership
from apps.shop.models import Shop, Order, OrderItem


class OrderException(Exception):
    pass


def update_order(order: Order, send_order_summary=False) -> Order:
    order_item_ids_processed = []

    for cart_index_string, cart_item in order.draft_cart.items():
        if not cart_index_string.startswith("i"):
            continue

        if 'item_id' not in cart_item:
            raise OrderException("missing item_id in cart item")
        if 'quantity' not in cart_item:
            raise OrderException("missing quantity in cart item")

        order_item = OrderItem.objects.none()
        if 'order_item_id' in cart_item:
            if cart_item['order_item_id'] in order_item_ids_processed:
                raise OrderException("duplicate order_item_id found")
            if cart_item['order_item_id']:
                order_item = OrderItem.objects.filter(id=cart_item['order_item_id']).first()

        if not order_item:
            order_item = OrderItem.objects.create(order=order)

        if cart_item.get('item_id') and cart_item.get('quantity'):
            order_item.item_id = cart_item['item_id']
            order_item.quantity = Decimal(cart_item['quantity'])

        order_item.save()
        order_item_ids_processed.append(order_item.id)

    order.order_items.exclude(id__in=order_item_ids_processed).delete()
    order.save()
    if send_order_summary:
        order.line_channel_membership.send_order_summary(order)

    return order


@start_new_thread
def async_update_order(order: Order, send_order_summary=False):
    update_order(order, send_order_summary)
    from django.db import connection
    connection.close()

import base64
import logging

from django.db import models
from apps.common.behaviors import Timestampable
from apps.common.utilities.multithreading import start_new_thread
from apps.line_app.models.line_rich_menu import MAIN_MENU, LineRichMenu
from django.utils.http import urlencode, urlsafe_base64_encode
from linebot.models import TextMessage, LocationMessage, ImageMessage, StickerMessage
from pinax.referrals.models import Referral

from apps.common.models import Image
from apps.line_app.views.delivery import Delivery
from apps.line_app.views.menu import Menu
from settings import HOSTNAME



class LineChannelMembership(Timestampable, models.Model):
    line_user_profile = models.ForeignKey('line_app.LineUserProfile', on_delete=models.CASCADE,
                                          related_name='line_channel_memberships')
    line_channel = models.ForeignKey('line_app.LineChannel', on_delete=models.CASCADE,
                                     related_name='line_channel_memberships')

    is_following = models.BooleanField(default=False)
    is_promotable = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text='user is admin or staff for line channel')

    # MODEL PROPERTIES
    @property
    def _uuid(self):
        return f"{self.line_channel.id}:{self.line_user_profile.line_user_id}"

    @property
    def url_safe_uuid(self):
        return urlsafe_base64_encode(bytes(self._uuid.encode()))
        # return base64.urlsafe_b64encode(bytes(self._uuid.encode())).decode()

    @property
    def current_rich_menu(self):
        return self.line_rich_menus.filter(_is_currently_active=True).first()

    # MODEL FUNCTIONS

    def set_rich_menu(self, index=MAIN_MENU, force_refresh=False):
        self.rich_menu, rm_created = LineRichMenu.objects.get_or_create(line_channel_membership=self, index=index)
        if force_refresh or not self.rich_menu.is_currently_active:
            self.rich_menu.publish_and_save(force_refresh=force_refresh)
            self.rich_menu.assign_to_user()
            self.rich_menu.save()


    def respond_to(self, line_event):

        if isinstance(line_event.message, TextMessage):
            if line_event.message.text.lower() == "menu":
                self.set_rich_menu(MAIN_MENU)
                return self.line_channel.welcome_text
            elif line_event.message.text.lower() == "order":
                menu = Menu()
                return menu.render_bot_message()

            elif line_event.message.text.lower() == "share":
                return self.line_channel.line_share_url

            elif line_event.message.text.lower() == "refer":
                referral = Referral.objects.get_or_create(
                    user=self.line_user_profile.user,
                    label="general",
                    redirect_to=self.line_channel.line_share_url
                )
                return referral.url

            elif line_event.message.text.lower() == "delivery":
                delivery = Delivery()
                return delivery.render_bot_message()

            elif line_event.message.text.lower() == "dashboard":
                # get link to shop dasbhoard and include otp login credentials
                if self.line_user_profile.user.is_staff or self.line_channel.shop == self.line_user_profile.user.shop:  # owner of shop
                    login_kwargs = {'username': self.line_user_profile.user.username, 'otp': self.line_user_profile.user.get_otp()}
                    return f"Manage {self.line_channel.shop.name} at " + f'https://{HOSTNAME}{self.line_channel.shop.get_absolute_url()}?{urlencode(login_kwargs)}'
                else:
                    return "sorry admins only 🤨"

            else:
                return "received " + line_event.message.text
        elif isinstance(line_event.message, ImageMessage):

            logging.debug(line_event.message.content_provider.original_content_url,
                          line_event.message.content_provider.preview_image_url)

            message_content = self.line_channel.get_bot().api.get_message_content(line_event.message.id)
            filename = '/tmp/some_image.unknown'
            with open(filename, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)

            empty_grammables = self.line_channel.shop.gramables.filter(url="", original_url="")
            if empty_grammables.exists():
                image = empty_grammables.first()
            else:
                image = Image.objects.create()
                self.line_channel.shop.gramables.add(image)

            image.upload_file(filename)
            image.save()

            if image.original_url:
                return "✓ photo saved"
            else:
                return "problem, Line didn't provide a url. I just got this: " + str(line_event.message.content_provider.__dict__)

        elif isinstance(line_event.message, LocationMessage):
            self.line_user_profile.save_location(line_event.message)
            return "Thanks! your location is saved 📍"
        else:
            return "🆗👍"


    def send_order_status(self, order):
        from apps.line_app.views.order_summary import OrderSummary
        from apps.shop.models.order import DRAFT, PLACED, SHOP_CONFIRMED, SHOP_COMPLETE, SHOP_REJECTED
        # assert(order in self.orders.all())

        if order.current_status == PLACED:
            order_summary = OrderSummary(order)
            self.line_channel.get_bot().api.push_message(
                self.line_user_profile.line_user_id,
                order_summary.render_bot_message()
            )
        elif order.current_status == SHOP_CONFIRMED:
            self.line_channel.get_bot().send_text_message(
                self.line_user_profile,
                f"Your server just confirmed your order. It's going to the kitchen now!"
            )
        elif order.current_status == SHOP_COMPLETE:
            self.line_channel.get_bot().send_text_message(
                self.line_user_profile,
                f"The kitchen just marked your order complete."
            )
        elif order.current_status == SHOP_REJECTED:
            self.line_channel.get_bot().send_text_message(
                self.line_user_profile,
                f"Order {order.id} has been cancelled. Check with your server if you need help."
            )

    @start_new_thread
    def run_async_rich_menu_check(self):
        if not self.current_rich_menu:
            self.set_rich_menu(force_refresh=False)
        from django.db import connection
        connection.close()

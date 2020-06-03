from django.db import models
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField
from django.contrib.postgres.fields import ArrayField
from apps.common.behaviors import Timestampable, Publishable, Expirable, Annotatable
from apps.shop.models.menu import PERIOD_CHOICES


class Item(Timestampable, Publishable, Expirable, Annotatable, models.Model):

    name = models.CharField(max_length=140, blank=False)
    description = models.TextField(default='', blank=True)
    image = models.OneToOneField('common.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='item')
    alt_images = models.ManyToManyField('common.Image', blank=True, related_name='items_as_alt_image')

    menu = models.ForeignKey('shop.Menu', null=False,
                             on_delete=models.PROTECT, related_name="items")
    menu_section = models.ForeignKey('shop.MenuSection', null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='items')
    # alt_menu_sections = models.ManyToManyField('shop.MenuSection', blank=True, related_name='alt_items')

    # calories_count = models.PositiveIntegerField(null=True, blank=True, help_text="amount of calories in this menu item")
    # allergies = ArrayField(models.CharField(max_length=4, choices=FOOD_ALLERGY_CHOICES), default=list, blank=True)
    # feature_ingredients = models.ManyToManyField('production.FoodIngredient', blank=True)
    # kitchen_goods = models.ManyToManyField('production.Good', blank=True)

    is_addon = models.BooleanField(default=False, help_text="can be topping or extra for addon another item")
    items_for_addon = models.ManyToManyField('shop.Item', blank=True, related_name='addon_items',
                                             help_text="other items this can be added onto")
    show_on_menu = models.BooleanField(default=True)
    show_on_menu_position = models.PositiveIntegerField(null=True, blank=True,
                                                        help_text="position within menu section when menu sections have positions")

    price = MoneyField(max_digits=8, decimal_places=2, null=True, default_currency='THB')
    # promotion - Promotion model has item, promo_price, Publishable, Expirable

    unavailable_periods = ArrayField(
        models.CharField(choices=PERIOD_CHOICES, max_length=4), default=list, blank=True
    )

    # HISTORY MANAGER
    history = HistoricalRecords()

    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def __str__(self):
        return f"{self.name} - {self.menu_section.name+' ' if self.menu_section else ''} at {self.menu.shop.name}"

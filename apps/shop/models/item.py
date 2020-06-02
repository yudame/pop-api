from django.db import models
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField
from django.contrib.postgres.fields import ArrayField
from apps.common.behaviors import Timestampable, Publishable, Expirable, Annotatable
from apps.shop.models.menu import PERIOD_CHOICES


class Item(Timestampable, Publishable, Expirable, Annotatable, models.Model):

    name = models.CharField(max_length=140, blank=False)
    description = models.TextField(default='', blank=True)
    image = models.OneToOneField('common.Image', null=True, on_delete=models.SET_NULL, related_name='item')
    alt_images = models.ManyToManyField('common.Image', related_name='items_as_alt_image')

    menu = models.ForeignKey('shop.Menu', null=False,
                             on_delete=models.PROTECT, related_name="items")
    menu_section = models.ForeignKey('shop.MenuSection', null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='items')
    # alt_menu_sections = models.ManyToManyField('shop.MenuSection', related_name='alt_items')

    # allergies = models.ManyToManyField('common.FoodAllergy')
    # feature_ingredients = models.ManyToManyField('common.FoodIngredient')
    # kitchen_goods = models.ManyToManyField('production.Good')

    price = MoneyField(max_digits=8, decimal_places=2, null=True, default_currency='THB')
    # promotion_price - Promotion model has item, promo_price, Publishable, Expirable

    unavailable_periods = ArrayField(
        models.CharField(choices=PERIOD_CHOICES, max_length=4), default=list
    )

    # HISTORY MANAGER
    history = HistoricalRecords()

    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def __str__(self):
        return f"{self.shop.name} Menu"

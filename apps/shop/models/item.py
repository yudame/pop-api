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

    calories_count = models.PositiveIntegerField(null=True, blank=True,
        help_text="amount of calories in this menu item")
    # allergies = ArrayField(models.CharField(max_length=4, choices=FOOD_ALLERGY_CHOICES), default=list, blank=True)
    # feature_ingredients = models.ManyToManyField('production.FoodIngredient', blank=True)
    # kitchen_goods = models.ManyToManyField('production.Good', blank=True)

    options_required_count = models.SmallIntegerField(null=True, blank=True,
        help_text='number of options that must be selected (eg. 2 on half/half pizza)')

    is_option = models.BooleanField(default=False,
        help_text="can be a required option for another item (eg. meat choice in a wrap)")
    items_for_option = models.ManyToManyField('shop.Item', blank=True, related_name='option_items',
        help_text="item(s) this can be an option on")
    option_price = MoneyField(max_digits=8, decimal_places=2, null=True, blank=True, default_currency='THB',
        help_text='price when option on another item')


    # items_for_addon = models.ManyToManyField('shop.Item', blank=True, related_name='addon_items',
    #     help_text="item(s) this can be added onto")
    # # to be deleted


    groups_of_addons = models.ManyToManyField('shop.AddonGroup', blank=True, through='shop.ItemAddonGroups', related_name='items_as_addon_group',
        help_text='types of addons that can be added (eg. salad dressings, toppings)')

    groups_as_addon = models.ManyToManyField('shop.AddonGroup', blank=True, through='shop.ItemAddonGroupMemberships', related_name='member_addon_items',
        help_text='types of addons this can be (eg. mushrooms as a pizza topping)')

    is_display_on_menu = models.BooleanField(default=True, help_text='can be ordered as standalone item')
    display_on_menu_position = models.PositiveIntegerField(null=True, blank=True,
        help_text="position within menu section when menu sections have positions")



    price = MoneyField(max_digits=8, decimal_places=2, null=True, blank=True, default_currency='THB',
        help_text='standalone order price')
    # promotion - Promotion model has item, promo_price, Publishable, Expirable

    unavailable_periods = ArrayField(
        models.CharField(choices=PERIOD_CHOICES, max_length=4), default=list, blank=True,
        help_text='list of period choices when unavailable (eg. [\'bf\',\'ln\'] for breakfast, lunch)')

    # HISTORY MANAGER
    # history = HistoricalRecords()

    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def __str__(self):
        try:
            group = self.menu_section.name if self.menu_section else ",".join([g.name for g in self.groups_as_addon.all()])
            return f"{self.name} | {group+' |' if group else ''} {self.menu.shop.name}"
        except:
            return self.name or self.id

    class Meta:
        ordering = ('display_on_menu_position',)
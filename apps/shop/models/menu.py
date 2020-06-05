from django.db import models
from simple_history.models import HistoricalRecords
from apps.common.behaviors import Timestampable

BREAKFAST, LUNCH, DINNER, BRUNCH = 'bf', 'ln', 'dn', 'br'
PERIOD_CHOICES = [
    (BREAKFAST, 'breakfast'),
    (LUNCH, 'lunch'),
    (DINNER, 'dinner'),
    (BRUNCH, 'brunch'),
]

class Menu(Timestampable, models.Model):

    shop = models.OneToOneField('shop.Shop', on_delete=models.PROTECT, related_name="menu")

    header_text = models.TextField(default="", blank=True)
    footer_text = models.TextField(default="", blank=True)

    # cuisines - ('thai', 'western', 'italian', 'indian', 'international', 'mediterranean', 'burgers', 'pizza', )
    # https: // en.wikipedia.org / wiki / List_of_cuisines

    # SETTINGS
    breakfast_open_time = models.TimeField(null=True, blank=True)
    breakfast_close_time = models.TimeField(null=True, blank=True)
    brunch_open_time = models.TimeField(null=True, blank=True)
    brunch_close_time = models.TimeField(null=True, blank=True)
    lunch_open_time = models.TimeField(null=True, blank=True)
    lunch_close_time = models.TimeField(null=True, blank=True)
    dinner_open_time = models.TimeField(null=True, blank=True)
    dinner_close_time = models.TimeField(null=True, blank=True)


    # HISTORY MANAGER
    history = HistoricalRecords()

    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def __str__(self):
        return f"{self.shop.name} Menu"


class MenuCategory(models.Model):

    name = models.CharField(max_length=50)
    parent = models.ForeignKey('shop.MenuCategory', null=True, blank=True,
                               on_delete=models.PROTECT, related_name='children')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Menu Categories"


class MenuSection(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    menu = models.ForeignKey('shop.Menu', on_delete=models.CASCADE, related_name='menu_sections')
    menu_category = models.ForeignKey('shop.MenuCategory',
                                      on_delete=models.PROTECT, related_name='menu_sections')
    is_display_on_menu = models.BooleanField(default=True)
    display_on_menu_position = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.menu_category.name})"

    class Meta:
        verbose_name_plural = "Menu Sections"

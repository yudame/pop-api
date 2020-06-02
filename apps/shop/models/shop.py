from django.db import models
from django.utils.text import slugify
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES
from simple_history.models import HistoricalRecords

from apps.common.behaviors import Timestampable, Locatable, Contactable, Translatable
from settings import AUTH_USER_MODEL


class Shop(Timestampable, Locatable, Contactable, Translatable, models.Model):

    owner = models.OneToOneField(AUTH_USER_MODEL, related_name="artist", on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(default="")
    square_logo_src = models.URLField(default="", blank=True)

    # SOCIAL ACCOUNTS
    facebook_href = models.URLField(default="", blank=True)
    instagram_href = models.URLField(default="", blank=True)
    google_maps_href = models.URLField(default="", blank=True)

    # SETTINGS
    is_ghost_location = models.BooleanField(default=False)
    currency = CurrencyField(default='THB')

    # inherited fields:
    # address, latitude, longitude
    # contact_name, contact_phone, contact_email
    # base_language, language


    # HISTORY MANAGER
    history = HistoricalRecords()

    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def __str__(self):
        return self.name or f"Shop {self.id}"

    def get_slug(self):
        return slugify(self.name)

    # META
    class Meta:
        ordering = ('name',)
        unique_together = ('owner', 'name')

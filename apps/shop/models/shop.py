from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from apps.common.behaviors import Timestampable, Locatable
from settings import AUTH_USER_MODEL


class Shop(Timestampable, Locatable, models.Model):

    owner = models.OneToOneField(AUTH_USER_MODEL, related_name="artist", on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=50, null=False)

    description = models.TextField(default="")
    square_logo_src = models.URLField(default="", blank=True)

    # SOCIAL ACCOUNTS
    facebook_href = models.URLField(default="", blank=True)
    instagram_href = models.URLField(default="", blank=True)
    google_maps_href = models.URLField(default="", blank=True)

    # SETTINGS
    is_ghost_location = models.BooleanField(default=False)

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

from django.db import models
from timezone_field import TimeZoneField


class Locatable(models.Model):

    address = models.ForeignKey('common.Address', null=True, blank=True, on_delete=models.SET_NULL)
    timezone = TimeZoneField(blank=True)

    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    # What 3 Words: https://developer.what3words.com/tutorial/python/
    # what3words = models.CharField(max_length=25?)

    class Meta:
        abstract = True

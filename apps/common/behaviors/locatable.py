from django.db import models
from timezone_field import TimeZoneField


class Locatable(models.Model):

    unstructured_text_address = models.TextField(default="", blank=True)
    address = models.ForeignKey('common.Address', null=True, blank=True, on_delete=models.SET_NULL)

    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    # What 3 Words: https://developer.what3words.com/tutorial/python/
    # what3words = models.CharField(max_length=25?)

    timezone = TimeZoneField(blank=True)

    def __str__(self):
        if self.address and len(self.address.inline_string):
            return self.address.inline_string
        elif self.unstructured_text_address:
            return self.unstructured_text_address
        elif self.longitude and self.latitude:
            return f"{self.latitude}, {self.longitude}"
        else:
            return "(no address)"

    class Meta:
        abstract = True

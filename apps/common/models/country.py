import uuid
from django.db import models
from djmoney.models.fields import MoneyField, CurrencyField


class Country(
        models.Model):  # could expand on pypi.python.org/pypi/django-countries

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=3, blank=True)
    calling_code = models.CharField(max_length=3, blank=True)

    # assuming countries stick to one currency nationwide
    currency = CurrencyField(help_text='default currency for the country', null=True, blank=True)

    # MODEL PROPERTIES

    # MODEL FUNCTIONS
    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name_plural = 'countries'

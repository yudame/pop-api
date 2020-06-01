from django.db import models


class Contactable(models.Model):
    primary_phone_number = models.CharField(max_length=15, null=True, blank=True)
    secondary_phone_number = models.CharField(max_length=15, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    sales_email = models.EmailField(null=True, blank=True)

    class Meta:
        abstract = True

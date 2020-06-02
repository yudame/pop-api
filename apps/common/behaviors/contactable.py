from django.db import models


class Contactable(models.Model):
    contact_name = models.CharField(max_length=50, blank=True, help_text="name of point of contact")
    contact_phone_number = models.CharField(max_length=15, blank=True, help_text='public contact phone')
    contact_email = models.EmailField(blank=True, help_text='public contact email')

    class Meta:
        abstract = True

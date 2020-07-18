from django.db import models
from fontawesome_5.fields import IconField


class Achievement(models.Model):

    name = models.CharField(max_length=50)
    icon = IconField(blank=True)
    point_value = models.SmallIntegerField(default=0, blank=True)

    class Meta:
        abstract = True

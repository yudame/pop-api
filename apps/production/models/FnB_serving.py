from django_measurement.models import MeasurementField
from measurement.measures import Volume, Mass

from django.db import models


class FnBServing(models.Model):

    good = models.ForeignKey('production.Good')

    ingredient_mass = MeasurementField(measurement=Volume, blank=True, null=True)
    ingredient_volume = MeasurementField(measurement=Volume, blank=True, null=True)

    serving_mass = MeasurementField(measurement=Mass, blank=True, null=True)
    serving_volume = MeasurementField(measurement=Mass, blank=True, null=True)

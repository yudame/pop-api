from django.contrib.postgres.fields import JSONField
from django.db import models


class AbstractEvent(models.Model):

    timestamp = models.DateTimeField()
    duration_seconds = models.DurationField(null=True, blank=True)
    source = models.ForeignKey('source.Source', on_delete=models.CASCADE)
    original_event_data = JSONField(default=dict())

    # MODEL PROPERTIES

    # MODEL FUNCTIONS

    class Meta:
        abstract = True

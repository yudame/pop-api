import uuid
from django.db import models
from apps.common.behaviors import Timestampable, Authorable


class TrelloObject(Timestampable, models.Model):

    trello_id = models.CharField(max_length=24, null=False)
    trello_url = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True

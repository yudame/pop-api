from django.db import models
from apps.common.behaviors import Timestampable, Permalinkable, Publishable


class BlogObject(Timestampable, Publishable, Permalinkable, models.Model):

    class Meta:
        abstract = True


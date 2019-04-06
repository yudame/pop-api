import uuid
from django.db import models
from apps.common.behaviors import Timestampable, Authorable, Permalinkable, Publishable


class BlogObject(Timestampable, Permalinkable, models.Model):

    class Meta:
        abstract = True


class Blog(BlogObject):
    title = models.CharField(max_length=120, null=False)
    parent_blog = models.ForeignKey("self")
    trello_board = models.ForeignKey("trello.Board")



class Topic(BlogObject):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120, null=False)
    description = models.TextField(default="", blank=True)

    # MODEL PROPERTIES

    # MODEL FUNCTIONS


class Article(Authorable, Publishable, BlogObject):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120, null=False)
    markdown = models.TextField(default="", blank=True)
    topics = models.ManyToManyField("Topic", related_name='articles')
    keywords = models.CharField(max_length=200, null=False)

    # MODEL PROPERTIES

    # MODEL FUNCTIONS

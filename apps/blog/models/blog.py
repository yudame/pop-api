import uuid
from django.db import models
from apps.common.behaviors import Timestampable, Authorable, Permalinkable, Publishable


class BlogObject(Timestampable, Permalinkable, models.Model):

    class Meta:
        abstract = True


class Blog(BlogObject):
    trello_board = models.ForeignKey("trello.Board", on_delete=models.CASCADE)
    parent_blog = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    # MODEL PROPERTIES
    @property
    def title(self):
        return self.trello_board.name

    # MODEL FUNCTIONS


class Topic(BlogObject):
    # trello_label = models.ForeignKey("trello.Label", on_delete=models.CASCADE)
    description = models.TextField(default="", blank=True)

    # MODEL PROPERTIES
    # @property
    # def title(self):
    #     return self.trello_label.name



class Article(Authorable, Publishable, BlogObject):
    trello_card = models.ForeignKey("trello.Card", on_delete=models.CASCADE)

    # topics = models.ManyToManyField("Topic", related_name='articles')
    # keywords = models.CharField(max_length=200, null=False)


    # MODEL PROPERTIES
    @property
    def title(self):
        return self.trello_card.name

    @property
    def markdown(self):
        return self.trello_card.markdown


    # MODEL FUNCTIONS

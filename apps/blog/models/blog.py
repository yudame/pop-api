import uuid
from django.db import models
from apps.common.behaviors import Timestampable, Authorable, Permalinkable, Publishable


class BlogObject(Timestampable, Publishable, Permalinkable, models.Model):

    class Meta:
        abstract = True


class Blog(BlogObject):
    trello_board = models.OneToOneField("trello.Board",
                                        related_name="blog", on_delete=models.CASCADE)
    parent_blog = models.ForeignKey("self", null=True, blank=True,
                                    related_name="child_blogs", on_delete=models.SET_NULL)

    # MODEL PROPERTIES
    @property
    def slug_source(self):
        return self.trello_board.name

    @property
    def title(self):
        return self.trello_board.name

    # MODEL FUNCTIONS


class Topic(BlogObject):
    trello_label = models.OneToOneField("trello.Label", related_name="topic", on_delete=models.CASCADE)
    blog = models.ForeignKey("blog.Blog", related_name="topics", on_delete=models.CASCADE)
    description = models.TextField(default="", blank=True)

    # MODEL PROPERTIES
    @property
    def slug_source(self):
        return self.trello_label.name

    # @property
    # def title(self):
    #     return self.trello_label.name



class Article(BlogObject):
    trello_card = models.OneToOneField("trello.Card", related_name="article", on_delete=models.CASCADE)
    blog = models.ForeignKey("blog.Blog", related_name="articles", on_delete=models.CASCADE)

    # topics = models.ManyToManyField("Topic", related_name='articles')
    # keywords = models.CharField(max_length=200, null=False)


    # MODEL PROPERTIES
    @property
    def slug_source(self):
        return self.trello_card.name

    @property
    def title(self):
        return self.trello_card.name

    @property
    def markdown(self):
        return self.trello_card.markdown


    # MODEL FUNCTIONS

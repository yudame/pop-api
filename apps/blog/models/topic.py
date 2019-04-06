from django.db import models
from django.urls import reverse
from apps.blog.models.abstract import BlogObject



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


from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.blog.models.abstract import BlogObject


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

    def get_absolute_url(self):
        return reverse('blog:blog', kwargs={'blog_slug': self.slug})



#
# @receiver(pre_save, sender=Blog)
# def pre_save_slug(sender, instance, *args, **kwargs):
#
#     if not instance.slug:
#         instance.slug = slugify(instance.slug_source)

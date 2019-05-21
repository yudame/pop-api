import socket

from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.blog.models.abstract import BlogObject
from django.contrib.sites.models import Site


class Blog(BlogObject):
    trello_board = models.OneToOneField("trello.Board",
                                        related_name="blog", on_delete=models.CASCADE)
    sites = models.OneToOneField(Site, on_delete=models.PROTECT)
    # parent_blog = models.ForeignKey("self", null=True, blank=True,
    #                                 related_name="child_blogs", on_delete=models.SET_NULL)

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

    def get_about_absolute_url(self):
        return reverse('blog:about', kwargs={'blog_slug': self.slug})

    def get_topics_absolute_url(self):
        return reverse('blog:topics', kwargs={'blog_slug': self.slug})




@receiver(pre_save, sender=Blog)
def pre_save_create_site(sender, instance, *args, **kwargs):
    if not instance.site:

        try:
            domain = f"{instance.slug}.{socket.gethostname()}"
        except:
            domain = 'localhost:8000'

        instance.site, created = Site.objects.get_or_create(domain=domain, name=instance.title)

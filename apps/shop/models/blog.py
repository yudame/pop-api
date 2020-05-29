import socket

from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.shop.models.abstract import BlogObject
from django.contrib.sites.models import Site


class Blog(BlogObject):

    # parent_blog = models.ForeignKey("self", null=True, blank=True,
    #                                 related_name="child_blogs", on_delete=models.SET_NULL)
    trello_board = models.OneToOneField("trello.Board", related_name="blog", on_delete=models.CASCADE)
    site = models.OneToOneField(Site, null=True, related_name="blog", on_delete=models.PROTECT)

    trello_board = models.OneToOneField("trello.Board", related_name="blog", on_delete=models.CASCADE)
    site = models.OneToOneField(Site, null=True, related_name="blog", on_delete=models.SET_NULL)

    # parent_blog = models.ForeignKey("self", null=True, blank=True,
    #                                 related_name="child_blogs", on_delete=models.SET_NULL)

    background_src = models.URLField(null=True, blank=True)
    logo_src = models.URLField(null=True, blank=True)
    _title = models.CharField(max_length=128, null=True, blank=True)
    _description = models.TextField(default="", blank=True)
    show_skibi_credits = models.BooleanField(default=True)
    footer_text = models.TextField(default="", blank=True)

    theme = models.ForeignKey("blog.Theme", related_name='blogs', on_delete=models.PROTECT,
                              null=True, blank=True)

    # MODEL PROPERTIES
    @property
    def slug_source(self):
        return self.trello_board.name

    @property
    def title(self):
        return self._title or self.trello_board.name or ""

    @property
    def description(self):
        return self._description or self.trello_board.description or ""

    # MODEL FUNCTIONS

    def get_absolute_url(self):
        return reverse('blog:blog', kwargs={'blog_slug': self.slug})

    def get_about_absolute_url(self):
        return reverse('blog:about', kwargs={'blog_slug': self.slug})

    def get_topics_absolute_url(self):
        return reverse('blog:topics', kwargs={'blog_slug': self.slug})

    def __str__(self):
        return self.title or f"Blog {self.id}"


@receiver(pre_save, sender=Blog)
def pre_save_create_site(sender, instance, *args, **kwargs):
    if not instance.site:
        try:
            domain = f"{instance.slug}.{socket.gethostname()}"
        except:
            domain = 'localhost:8000'

        instance.site, created = Site.objects.get_or_create(domain=domain, name=instance.title)

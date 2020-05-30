from django.db import models
from django.urls import reverse

from apps.website.models.abstract import BlogObject



class Topic(BlogObject):
    trello_label = models.OneToOneField("trello.Label", related_name="topic", on_delete=models.CASCADE)
    website = models.ForeignKey("shop.Website", related_name="topics", on_delete=models.CASCADE)
    description = models.TextField(default="", blank=True)

    # MODEL PROPERTIES
    @property
    def slug_source(self):
        return self.trello_label.name

    @property
    def title(self):
        return self.trello_label.name

    @property
    def articles(self):
        from apps.shop.models import Article
        return Article.objects.filter(trello_card_id__in=[card.id for card in self.trello_label.cards.all()])

    # MODEL FUNCTIONS

    def get_absolute_url(self):
        return reverse('website:topic', kwargs={'website_slug': self.website.slug, 'topic_slug': self.slug})

from django.db import models
from django.urls import reverse
from apps.website.models.abstract import BlogObject


class Article(BlogObject):
    trello_card = models.OneToOneField("trello.Card", related_name="article", on_delete=models.CASCADE)
    website = models.ForeignKey("shop.Website", related_name="articles", on_delete=models.CASCADE)

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

    @property
    def topics(self):
        from apps.website.models import Topic
        return Topic.objects.filter(trello_label_id__in=[label.id for label in self.trello_card.labels.all()])


    # MODEL FUNCTIONS

    def get_absolute_url(self):
        return reverse('website:article', kwargs={'website_slug': self.website.slug, 'article_slug': self.slug})


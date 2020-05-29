import uuid
from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.trello.models.abstract import TrelloObject


class Card(TrelloObject):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # board = models.ForeignKey("Board", null=False, on_delete=models.CASCADE, related_name="cards")# use self.list.board
    list = models.ForeignKey("List", null=False, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=120, null=False)
    markdown = models.TextField(default="", blank=True)
    labels = models.ManyToManyField("Label", related_name="cards")
    is_closed = models.BooleanField(default=False)


    # MODEL PROPERTIES

    @property
    def short_url(self):
        return f"https://trello.com/c/{self.trello_shortlink}"

    # MODEL FUNCTIONS



# load card and make article
@receiver(post_save, sender=Card)
def post_save(instance, *args, **kwargs):
    if instance.is_closed:
        try:
            instance.article.unpublished_at = datetime.now()
            instance.article.save()
        except:
            pass
    else:
        from apps.shop.models import Article
        # from apps.trello.trello import client
        # t_card = client.get_card(instance.trello_id)

        article, created = Article.objects.get_or_create(
            trello_card=instance,
            blog=instance.list.board.blog
        )

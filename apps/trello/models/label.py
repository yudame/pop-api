import uuid
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.trello.models.abstract import TrelloObject


class Label(TrelloObject):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey("Board", null=False, on_delete=models.CASCADE, related_name="labels")
    name = models.CharField(max_length=120, null=False)
    color = models.CharField(max_length=15, null=True, blank=True)


    # MODEL PROPERTIES

    @property
    def short_url(self):
        return f"https://trello.com/c/{self.trello_shortlink}"

    # MODEL FUNCTIONS


# load label and make topic
@receiver(post_save, sender=Label)
def post_save(instance, *args, **kwargs):
    from apps.blog.models import Topic
    # from apps.trello.trello import client
    # t_card = client.get_card(instance.trello_id)

    topic, created = Topic.objects.get_or_create(
        trello_label=instance,
        blog=instance.board.blog
    )

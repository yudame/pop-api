import uuid
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.trello.models.abstract import TrelloObject



class List(TrelloObject):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey("Board", null=False, on_delete=models.CASCADE, related_name="lists")
    name = models.CharField(max_length=120, null=False)
    position = models.FloatField(null=False)
    is_closed = models.BooleanField(default=False)

    # MODEL PROPERTIES

    # MODEL FUNCTIONS



# reset all list details
@receiver(pre_save, sender=List)
def pre_save(instance, *args, **kwargs):
    from apps.trello.trello import client
    t_list = client.get_list(instance.trello_id)
    instance.trello_id = t_list.id
    instance.name = t_list.name
    instance.position = t_list.pos
    instance.is_closed = t_list.closed


# load list and make cards
@receiver(post_save, sender=List)
def pre_save(instance, *args, **kwargs):
    from apps.trello.models.card import Card
    from apps.trello.models import Label
    from apps.trello.trello import client
    t_list = client.get_list(instance.trello_id)
    t_cards = t_list.list_cards()
    if not t_cards:
        return
    for t_card in t_cards:
        if t_card.name:
            card, created = Card.objects.get_or_create(
                trello_id=t_card.id,
                trello_url=t_card.url,
                list=instance,
                name=t_card.name,
                markdown=t_card.description,
            )
            if not t_card.labels:
                continue
            for t_label in t_card.labels:
                card.labels.add(Label.objects.get(trello_id=t_label.id))

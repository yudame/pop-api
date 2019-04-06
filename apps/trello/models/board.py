import uuid
from django.db import models
from apps.common.behaviors import Timestampable, Authorable


class TrelloObject(Timestampable, models.Model):

    trello_id = models.CharField(max_length=24, null=False)
    trello_shortlink = models.CharField(max_length=8, null=False)

    class Meta:
        abstract = True



class Board(TrelloObject):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, null=False)
    is_closed = models.BooleanField(default=False)

    # MODEL PROPERTIES

    @property
    def short_url(self):
        return f"https://trello.com/b/{self.trello_shortlink}"

    # MODEL FUNCTIONS



class List(TrelloObject):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey("Board", null=False, on_delete=models.CASCADE, related_name="lists")
    name = models.CharField(max_length=120, null=False)
    position = models.SmallIntegerField(null=False)
    is_closed = models.BooleanField(default=False)

    # MODEL PROPERTIES

    # MODEL FUNCTIONS



class Card(TrelloObject):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # board = models.ForeignKey("Board", null=False)  # use self.list.board
    list = models.ForeignKey("List", null=False, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=120, null=False)
    markdown = models.TextField(default="", blank=True)
    labels = models.TextField(default="", blank=True)


    # MODEL PROPERTIES

    @property
    def short_url(self):
        return f"https://trello.com/c/{self.trello_shortlink}"

    # MODEL FUNCTIONS


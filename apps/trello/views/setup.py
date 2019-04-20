from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.base import View
from apps.trello.models import Board

from settings import HOSTNAME


class SetupView(View):
    def dispatch(self, request, board_id, *args, **kwargs):
        self.board, created = Board.objects.get_or_create(trello_id=board_id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        from apps.trello.trello import client

        callback_url = HOSTNAME + reverse('trello:callback', kwargs={})

        client.create_hook(
            callback_url,
            self.board.trello_id,
            desc="publish board changes"
        )

        return HttpResponse(status=200)  # ok

from django.contrib import admin
from apps.trello.models import Board, List, Card


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    pass

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass

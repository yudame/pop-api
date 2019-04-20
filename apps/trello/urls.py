from django.conf.urls import url

from apps.trello.views.setup import SetupView
from apps.trello.views.callback import CallbackView


app_name = 'trello'

urlpatterns = [

    url(r'^trello-setup', SetupView.as_view(), name='setup'),

    url(r'^trello-callback', CallbackView.as_view(), name='callback'),

]

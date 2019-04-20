from django.conf.urls import url

from apps.trello.views.setup import AuthView, SetupView
from apps.trello.views.callback import CallbackView


app_name = 'trello'

urlpatterns = [

    url(r'^setup', SetupView.as_view(), name='setup'),  # for manual setup

    url(r'^auth', AuthView.as_view(), name='auth'),

    url(r'^callback', CallbackView.as_view(), name='callback'),

]

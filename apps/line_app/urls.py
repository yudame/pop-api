from django.urls import path
from apps.line_app.views import main

app_name = "line_app"

urlpatterns = [
    path('', main.index, name='index'),
    path('callback/<uuid:line_channel_id>/', main.callback, name='callback'),
]

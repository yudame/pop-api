from django.urls import path
from apps.line_app.views import start

app_name = "line_app"

urlpatterns = [
    path('', start.index, name='index'),
    path('callback/', start.callback, name='callback'), # add this line
]

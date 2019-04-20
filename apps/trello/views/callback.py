from django.http import HttpResponse
from django.views.generic.base import View


class CallbackView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse(status=200)  # ok

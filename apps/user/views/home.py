from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    # def dispatch(self, request, *args, **kwargs):
    #     self.context = {}
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

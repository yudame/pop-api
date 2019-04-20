from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from apps.trello.models import Board


class AuthView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse(status=400)  # bad request

    def post(self, request):
        new_trello_board_id = request.POST.get("trello_board_id")

        try:
            board = Board.register_new_board(new_trello_board_id)
            return HttpResponse(status=200)  # ok
        except Exception as e:
            return HttpResponse(status=500, content=str(e))


class SetupForm(forms.Form):

    trello_board_url = forms.URLField(
            widget=forms.URLInput(),
            label="Trello Board URL",
            required=True)


class SetupView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        context = {
            'setup_form': SetupForm(),
        }
        return render(request, "setup.html", context=context)


    def post(self, request):

        setup_form = SetupForm(request.POST)

        if setup_form.is_valid():
            trello_board_url = request.POST.get("trello_board_url")
            trello_board_short_code = trello_board_url.split("/")[trello_board_url.split("/").index('b') + 1]

            try:
                board = Board.register_new_board(trello_board_short_code)
                messages.success(request, "Setup Successful.")

                return redirect('blog:blog', blog_slug = board.blog.slug)
            except Exception as e:
                return HttpResponse(status=500, content=str(e))


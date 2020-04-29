import re

from django import forms
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from apps.blog.models import Blog
from apps.trello.models import Board


class BlogView(View):
    def dispatch(self, request, blog_slug, *args, **kwargs):
        self.blog = get_object_or_404(Blog, slug=blog_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'blog': self.blog,
        }
        return render(request, 'blog.html', context)




class BlogSetupForm(forms.Form):
    trello_board = forms.URLField(label='Trello Board Link', min_length=18)
    subdomain = forms.CharField(label="Subdomain", validators=[validate_slug])



class BlogSetupView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        blog_setup_form = BlogSetupForm()


        context = {
            "blog_setup_form": blog_setup_form
        }
        return render(request, 'blog.html', context)

    def post(self, request):
        blog_setup_form = BlogSetupForm(request.POST)

        if blog_setup_form.is_valid():
            trello_board = blog_setup_form.cleaned_data["trello_board"]
            subdomain = blog_setup_form.cleaned_data["subdomain"]

            reg_expression = r'[a-zA-Z-:\/]*trello.com/b/(?P<trello_id>\w{8})/?[-a-z]*'

            found_ids = re.findall(reg_expression, trello_board)
            if not len(found_ids):
                raise ValidationError

            trello_board_id = found_ids[0]

            board, created = Board.objects.get_or_create(trello_id=trello_board_id, slug=subdomain)
            site, created = Site.objects.get_or_create(name=board.title)
            blog = board.blog
            blog.site = site
            blog.save()
            board.save()

            return redirect('blog:blog', blog_slug=blog.slug)
        else:
            context = {
                "blog_setup_form": blog_setup_form
            }
            return render(request, 'blog.html', context)

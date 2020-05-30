import re

from django import forms
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from apps.website.models import Website
from apps.trello.models import Board


class WebsiteView(View):
    def dispatch(self, request, website_slug, *args, **kwargs):
        self.website = get_object_or_404(Website, slug=website_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'website': self.website,
        }
        return render(request, 'website.html', context)




class WebsiteSetupForm(forms.Form):
    trello_board = forms.URLField(label='Trello Board Link', min_length=18)
    subdomain = forms.CharField(label="Subdomain", validators=[validate_slug])



class WebsiteSetupView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        website_setup_form = WebsiteSetupForm()


        context = {
            "website_setup_form": website_setup_form
        }
        return render(request, 'website.html', context)

    def post(self, request):
        website_setup_form = WebsiteSetupForm(request.POST)

        if website_setup_form.is_valid():
            trello_board = website_setup_form.cleaned_data["trello_board"]
            subdomain = website_setup_form.cleaned_data["subdomain"]

            reg_expression = r'[a-zA-Z-:\/]*trello.com/b/(?P<trello_id>\w{8})/?[-a-z]*'

            found_ids = re.findall(reg_expression, trello_board)
            if not len(found_ids):
                raise ValidationError

            trello_board_id = found_ids[0]

            board, created = Board.objects.get_or_create(trello_id=trello_board_id, slug=subdomain)
            site, created = Site.objects.get_or_create(name=board.title)
            website = board.website
            website.site = site
            website.save()
            board.save()

            return redirect('shop:website', website_slug=website.slug)
        else:
            context = {
                "website_setup_form": website_setup_form
            }
            return render(request, 'website.html', context)

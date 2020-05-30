from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.website.models import Article, Website


class ArticleView(View):
    def dispatch(self, request, website_slug, article_slug, *args, **kwargs):
        self.website = get_object_or_404(Website, slug=website_slug)
        self.article = get_object_or_404(Article, website__slug=website_slug, slug=article_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'website': self.website,
            'article': self.article,
        }
        return render(request, 'article.html', context)

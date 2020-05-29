from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.shop.models import Article, Blog


class ArticleView(View):
    def dispatch(self, request, blog_slug, article_slug, *args, **kwargs):
        self.blog = get_object_or_404(Blog, slug=blog_slug)
        self.article = get_object_or_404(Article, blog__slug=blog_slug, slug=article_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'blog': self.blog,
            'article': self.article,
        }
        return render(request, 'article.html', context)

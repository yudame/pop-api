from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.blog.models.blog import Article


class ArticleView(View):
    def dispatch(self, request, article_id, *args, **kwargs):
        self.article = get_object_or_404(Article, id=article_id)

    def get(self, request):
        context = {
            'article': self.article,
        }
        return render(request, 'article.html', context)

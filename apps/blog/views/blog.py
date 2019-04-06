from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.blog.models import Blog


class BlogView(View):
    def dispatch(self, request, blog_slug, *args, **kwargs):
        self.blog = get_object_or_404(Blog, slug=blog_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'blog': self.blog,
        }
        return render(request, 'blog.html', context)

from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.blog.models import Topic


class TopicView(View):
    def dispatch(self, request, blog_slug, topic_slug, *args, **kwargs):
        self.topic = get_object_or_404(Topic, blog__slug=blog_slug, slug=topic_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'topic': self.topic,
        }
        return render(request, 'topic.html', context)

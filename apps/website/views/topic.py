from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.website.models import Topic, Website


class TopicsView(View):
    def dispatch(self, request, website_slug, *args, **kwargs):
        self.website = get_object_or_404(Website, slug=website_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'website': self.website,
        }
        return render(request, 'topics.html', context)



class TopicView(View):
    def dispatch(self, request, website_slug, topic_slug, *args, **kwargs):
        self.website = get_object_or_404(Website, slug=website_slug)
        self.topic = get_object_or_404(Topic, website__slug=website_slug, slug=topic_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'website': self.website,
            'topic': self.topic,
        }
        return render(request, 'topic.html', context)

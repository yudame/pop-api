from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.blog.models import Topic


class TopicView(View):
    def dispatch(self, request, topic_id, *args, **kwargs):
        self.topic = get_object_or_404(Topic, id=topic_id)

    def get(self, request):
        context = {
            'topic': self.topic,
        }
        return render(request, 'topic.html', context)

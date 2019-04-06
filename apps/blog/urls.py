from django.conf.urls import url

from apps.blog.views.article import ArticleView
from apps.blog.views.topic import TopicView
from apps.blog.views.blog import BlogView

app_name = 'blog'

urlpatterns = [

    url(r'^(?P<blog_slug>[-\w\.]+)$',
        BlogView.as_view(), name='topic'),

    url(r'^topic/(?P<topic_id>[-\w\.]+)$',
        TopicView.as_view(), name='topic'),

    url(r'^article/(?P<article_id>[-\w\.]+)$',
        ArticleView.as_view(), name='article'),
]

from django.conf.urls import url

from apps.blog.views.article import ArticleView
from apps.blog.views.topic import TopicsView, TopicView
from apps.blog.views.blog import BlogView, BlogSetupView

app_name = 'blog'

urlpatterns = [

    url(r'^setup$',
        BlogSetupView.as_view(), name='setup'),

    url(r'^(?P<blog_slug>[-\w\.]+)$',
        BlogView.as_view(), name='blog'),

    url(r'^(?P<blog_slug>[-\w\.]+)/about$',
        TopicsView.as_view(), name='about'),

    url(r'^(?P<blog_slug>[-\w\.]+)/topics$',
        TopicsView.as_view(), name='topics'),

    url(r'^(?P<blog_slug>[-\w\.]+)/topic/(?P<topic_slug>[-\w\.]+)$',
        TopicView.as_view(), name='topic'),

    url(r'^(?P<blog_slug>[-\w\.]+)/article/(?P<article_slug>[-\w\.]+)$',
        ArticleView.as_view(), name='article'),
]

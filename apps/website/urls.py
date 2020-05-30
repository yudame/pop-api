from django.conf.urls import url

from apps.website.views.article import ArticleView
from apps.website.views.topic import TopicsView, TopicView
from apps.website.views.website import WebsiteView, WebsiteSetupView

app_name = 'website'

urlpatterns = [

    url(r'^setup$',
        WebsiteSetupView.as_view(), name='setup'),

    url(r'^(?P<website_slug>[-\w\.]+)$',
        WebsiteView.as_view(), name='website'),

    url(r'^(?P<website_slug>[-\w\.]+)/about$',
        TopicsView.as_view(), name='about'),

    url(r'^(?P<website_slug>[-\w\.]+)/topics$',
        TopicsView.as_view(), name='topics'),

    url(r'^(?P<website_slug>[-\w\.]+)/topic/(?P<topic_slug>[-\w\.]+)$',
        TopicView.as_view(), name='topic'),

    url(r'^(?P<website_slug>[-\w\.]+)/article/(?P<article_slug>[-\w\.]+)$',
        ArticleView.as_view(), name='article'),
]

from django.conf.urls import url

from apps.blog.views import article

urlpatterns = [

    # url(r'^$', home.Home.as_view(), name='home'),

    url(r'^topic/(?P<topic_id>[-\w\.]+)$',
        article.TopicView.as_view(), name='topic'),

    url(r'^article/(?P<article_id>[-\w\.]+)$',
        article.ArticleView.as_view(), name='article'),
]

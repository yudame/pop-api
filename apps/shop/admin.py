from django.contrib import admin
from apps.shop.models import Blog, Topic, Article, Link


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass

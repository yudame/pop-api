from django.contrib import admin
from apps.blog.models import Blog, Topic, Article


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

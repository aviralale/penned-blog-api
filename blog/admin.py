from django.contrib import admin
from .models import Blog, BlogView, Quote, Comment, Reply


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "author__username")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(BlogView)
class BlogViewAdmin(admin.ModelAdmin):
    list_display = ("blog", "session_id", "created_at")
    search_fields = ("blog__title", "session_id")


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("blog", "text", "author")
    search_fields = ("blog__title", "text", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("blog", "author", "created_at", "updated_at")
    search_fields = ("blog__title", "author__username", "content")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("comment", "author", "created_at", "updated_at")
    search_fields = ("comment__content", "author__username", "content")

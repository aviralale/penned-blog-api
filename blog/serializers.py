from rest_framework import serializers
from .models import Blog, Quote, Comment, Reply
from accounts.serializers import UserSerializer


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ["text", "author"]


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    quote1 = serializers.SerializerMethodField()
    quote2 = serializers.SerializerMethodField()
    quote3 = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "author",
            "created_at",
            "updated_at",
            "comment_count",
            "quote1",
            "quote2",
            "quote3",
            "view_count",
        ]

    def get_quote1(self, obj):
        quotes = obj.quotes.all()
        return QuoteSerializer(quotes[0]).data if quotes.exists() else None

    def get_quote2(self, obj):
        quotes = obj.quotes.all()
        return QuoteSerializer(quotes[1]).data if quotes.count() > 1 else None

    def get_quote3(self, obj):
        quotes = obj.quotes.all()
        return QuoteSerializer(quotes[2]).data if quotes.count() > 2 else None

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_view_count(self, obj):
        return obj.views.count()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "blog", "author", "content", "created_at", "updated_at"]


class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = [
            "id",
            "comment",
            "author",
            "content",
            "created_at",
            "updated_at",
            "blog",
        ]

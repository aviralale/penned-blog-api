from django.db.models import Count, Q
from django.utils.timezone import now, timedelta
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Blog, Comment, Reply, BlogView
from .serializers import BlogSerializer, CommentSerializer, ReplySerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by("-created_at")
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    lookup_field = "slug"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get"])
    def comments(self, request, slug=None):
        blog = self.get_object()
        comments = Comment.objects.filter(blog=blog)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def most_viewed(self, request):
        blogs = Blog.objects.annotate(view_count=Count("views")).order_by(
            "-view_count"
        )[:5]
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def most_recent(self, request):
        blogs = Blog.objects.all().order_by("-created_at")[:5]
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def most_viewed_month(self, request):
        one_month_ago = now() - timedelta(days=30)
        blogs = Blog.objects.annotate(
            view_count=Count("views", filter=Q(views__created_at__gte=one_month_ago))
        ).order_by("-view_count")[:5]
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-author/(?P<author_id>\d+)")
    def by_author(self, request, author_id=None):
        blogs = Blog.objects.filter(author_id=author_id).order_by("-created_at")
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def most_engaged(self, request):
        blogs = Blog.objects.annotate(
            engagement_count=Count("views") + Count("comments")
        ).order_by("-engagement_count")[:5]
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get"])
    def replies(self, request, pk=None):
        comment = self.get_object()
        replies = Reply.objects.filter(comment=comment)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all().order_by("-created_at")
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

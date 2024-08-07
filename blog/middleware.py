from django.utils.deprecation import MiddlewareMixin
from .models import Blog, BlogView


class BlogViewMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if "slug" in view_kwargs:
            try:
                blog = Blog.objects.get(slug=view_kwargs["slug"])
                session_id = request.session.session_key

                if not session_id:
                    request.session.create()
                    session_id = request.session.session_key

                if not BlogView.objects.filter(
                    blog=blog, session_id=session_id
                ).exists():
                    BlogView.objects.create(blog=blog, session_id=session_id)

            except Blog.DoesNotExist:
                pass

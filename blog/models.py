from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import User
from django.core.exceptions import ValidationError


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()

    def view_count(self):
        return self.views.count()


@receiver(pre_save, sender=Blog)
def create_blog_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class BlogView(models.Model):
    blog = models.ForeignKey(Blog, related_name="views", on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View for {self.blog.title} by session {self.session_id}"


class Quote(models.Model):
    blog = models.ForeignKey(Blog, related_name="quotes", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'"{self.text}" by {self.author}'

    def save(self, *args, **kwargs):
        if self.blog.quotes.count() >= 3:
            raise ValidationError("A blog can have a maximum of 3 quotes.")
        super().save(*args, **kwargs)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, related_name="replies", on_delete=models.CASCADE
    )
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

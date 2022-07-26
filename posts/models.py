from datetime import datetime
from django.db import models
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    def like(self, user):
        post_like, _ = PostLike.objects.get_or_create(user=user, post=self)

        if not post_like.is_liked:
            post_like.is_liked = True
            post_like.save()

    def unlike(self, user):
        post_like, _ = PostLike.objects.get_or_create(user=user, post=self)

        if post_like.is_liked:
            post_like.is_liked = False
            post_like.save()


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)
    timestamp = models.DateTimeField(blank=True, default=datetime.now())


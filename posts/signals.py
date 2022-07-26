import pytz

from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import PostLike, Post

@receiver(pre_save, sender=PostLike)
def post_like_update_timestamp(sender, instance: PostLike, **kwargs):
    instance.timestamp = datetime.now()

@receiver(pre_save, sender=Post)
def post_update_edited_timestamp(sender, instance: PostLike, **kwargs):
    if instance.id:
        instance.edited_timestamp = datetime.now().replace(tzinfo=pytz.UTC)


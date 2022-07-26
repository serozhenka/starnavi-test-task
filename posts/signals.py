from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import PostLike

@receiver(pre_save, sender=PostLike)
def post_like_update_timestamp(sender, instance: PostLike, **kwargs):
    instance.timestamp = datetime.now()

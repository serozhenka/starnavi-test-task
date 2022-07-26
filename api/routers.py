from rest_framework import routers

from .viewsets import PostViewSet

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status

from .serializers import PostSerializer
from posts.models import Post

class PostViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
    ):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        post = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = PostSerializer(post)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        return super().update(request, *args, **kwargs)

    def check_object_permissions(self, request, obj):
        if request.user != obj.user:
            raise PermissionDenied
        return True



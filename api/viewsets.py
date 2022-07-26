from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import mixins, viewsets

from .serializers import PostSerializer
from posts.models import Post

class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        post = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

post_retrieve = PostViewSet.as_view({'get': 'retrieve'})
post_list = PostViewSet.as_view({'get': 'list'})
post_create = PostViewSet.as_view({'post': 'create'})

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, views, response, status
from rest_framework.response import Response

from django.contrib.auth import login, logout

from .serializers import RegisterSerializer, LoginSerializer, PostSerializer
from posts.models import Post
from users.models import Account

class RegisterApiView(generics.CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginApiView(views.APIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return response.Response(None, status=status.HTTP_200_OK)


class PostCreateApiView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return response.Response(None, status=status.HTTP_200_OK)

class LogoutApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return response.Response(None, status=status.HTTP_200_OK)


class PostApiView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    lookup_field = 'pk'
    serializer_class = PostSerializer


class PostLikeApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        post = get_object_or_404(Post.objects.all(), pk=pk)
        post.like(request.user)
        return Response(None, status=status.HTTP_200_OK)


class PostUnlikeApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        post = get_object_or_404(Post.objects.all(), pk=pk)
        post.unlike(request.user)
        return Response(None, status=status.HTTP_200_OK)






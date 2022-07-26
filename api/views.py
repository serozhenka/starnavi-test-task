import pytz

from datetime import datetime
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, views, response, status, pagination
from rest_framework.response import Response

from django.contrib.auth import login, logout

from .serializers import RegisterSerializer, LoginSerializer, PostSerializer, PostLikeSerializer, SimpleAccountSerializer
from posts.models import Post, PostLike
from users.models import Account


class RegisterApiView(generics.CreateAPIView):

    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginApiView(views.APIView):

    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return Response([], status=status.HTTP_200_OK)

class LogoutApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response([], status=status.HTTP_200_OK)


# class PostCreateApiView(generics.CreateAPIView):
#
#     queryset = Post.objects.all()
#     serializer_class = LoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = PostSerializer(data=self.request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)
#
#
# class PostApiView(generics.ListCreateAPIView):
#
#     queryset = Account.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'pk'


class PostLikesView(generics.ListAPIView):

    serializer_class = PostLikeSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post.objects.all(), pk=pk)
        return post.postlike_set.filter(is_liked=True)


class PostLikeApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        post = get_object_or_404(Post.objects.all(), pk=pk)
        post.like(request.user)
        return Response([], status=status.HTTP_200_OK)


class PostUnlikeApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        post = get_object_or_404(Post.objects.all(), pk=pk)
        post.unlike(request.user)
        return Response([], status=status.HTTP_200_OK)


class PostLikesAnalyticsApiView(generics.ListAPIView):

    serializer_class = PostLikeSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        date_from, date_to = query_params.get('date_from'), self.request.query_params.get('date_to')

        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
        except Exception:
            date_from = datetime.min

        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
        except Exception:
            date_to = datetime.max

        date_from = date_from.replace(tzinfo=pytz.UTC)
        date_to = date_to.replace(tzinfo=pytz.UTC)

        post_likes = PostLike.objects.filter(
            is_liked=True,
            timestamp__gte=date_from,
            timestamp__lt=date_to,
        ).extra(
            select={'day': 'date( timestamp )'}
        ).values('day').annotate(likes_count=Count('timestamp')).order_by('-day')

        return post_likes

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return Response(list(qs))

class UserActivityApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(Account.objects.all(), pk=pk)

        info = {
            'user': SimpleAccountSerializer(user).data,
            'last_activity': user.last_activity,
            'last_login': user.last_login,
        }

        return Response(info)








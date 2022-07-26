from rest_framework import generics, permissions, views, response, status

from django.contrib.auth import login, logout

from .serializers import RegisterSerializer, LoginSerializer
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




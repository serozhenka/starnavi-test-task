from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views, viewsets
from .viewsets import post_retrieve
from .routers import router

urlpatterns = [
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('register/', views.RegisterApiView.as_view(), name='register'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('posts/<str:pk>/like/', views.PostLikeApiView.as_view(), name='posts-like'),
    path('posts/<str:pk>/unlike/', views.PostUnlikeApiView.as_view(), name='posts-unlike'),
]

urlpatterns += router.urls
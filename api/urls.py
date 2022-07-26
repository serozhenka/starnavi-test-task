from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .routers import router

urlpatterns = [
    path('users/<str:pk>/activity/', views.UserActivityApiView.as_view(), name='user-activity'),

    path('login/', views.LoginApiView.as_view(), name='login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('register/', views.RegisterApiView.as_view(), name='register'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('posts/<str:pk>/like/', views.PostLikeApiView.as_view(), name='posts-like'),
    path('posts/<str:pk>/unlike/', views.PostUnlikeApiView.as_view(), name='posts-unlike'),
    path('posts/<str:pk>/likes/', views.PostLikesView.as_view(), name='posts-likes'),
    path('posts/likes/analytics/', views.PostLikesAnalyticsApiView.as_view(), name='posts-likes-analytics'),

]

urlpatterns += router.urls
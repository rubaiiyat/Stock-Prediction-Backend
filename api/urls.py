from django.urls import path
from accounts.views import RegisterCreateAPIView,MeAPIView,LogoutAPIView,RefreshAPIView,LoginAPIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('auth/register/',RegisterCreateAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path("auth/refresh/", RefreshAPIView.as_view()),
    path('auth/me/',MeAPIView.as_view()),
    path('auth/logout/',LogoutAPIView.as_view()),
]

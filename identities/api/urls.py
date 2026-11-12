from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProfileView, SigninView, SignoutView, SignupView

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/signin/", SigninView.as_view(), name="signin"),
    path("auth/signout/", SignoutView.as_view(), name="signout"),
    path("auth/jwt/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]


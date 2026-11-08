from django.urls import path
from .views import ProfileView, SigninView, SignoutView, SignupView

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/signin/", SigninView.as_view(), name="signin"),
    path("auth/signout/", SignoutView.as_view(), name="signout"),
    path("profile/", ProfileView.as_view(), name="profile"),
]


from django.contrib.auth.views import LoginView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import RegisterView, UserProfileView, LogoutView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
from django.contrib.auth.views import PasswordResetView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import RegisterView, UserProfileView, LogoutView, LoginView, ForgotPasswordView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),   # <-- use your custom API LoginView
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", PasswordResetView.as_view(), name="reset_password"),
]

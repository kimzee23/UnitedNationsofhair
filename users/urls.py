from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import RegisterView, UserProfileView, LoginView, ForgotPasswordView, RequestOTPView, \
    VerifyOTPView, VerifyEmailView, ApplyForUpgradeView, ApproveUpgradeView, RejectUpgradeView, ResetPasswordView, \
    LogoutView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("request-otp/", RequestOTPView.as_view(), name="request_otp"),
    path("verify-otp", VerifyOTPView.as_view(), name="verify_otp"),
    path("verify-email", VerifyEmailView.as_view(), name="verify_email"),

    path("apply-upgrade/", ApplyForUpgradeView.as_view(), name="apply-upgrade"),
    path("approve-upgrade/<uuid:user_id>/", ApproveUpgradeView.as_view(), name="approve-upgrade"),
    path("reject-upgrade/<uuid:user_id>/", RejectUpgradeView.as_view(), name="reject-upgrade"),


]



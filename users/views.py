from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from users.models import User
from users.otp_models import EmailOTP
from users.serializers import (
    RegisterSerializer,
    UserSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    RequestOTPSerializer,
    VerifyOTPSerializer, VendorApplicationSerializer,
)

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token),
            "refresh": str(refresh)
            }


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = default_token_generator.make_token(user)
        verify_url = f"{settings.FRONTEND_URL}/verify-email/?uid={user.pk}&token={token}"

        send_mail(
            subject="Verify your email",
            message=f"Click here to verify your account: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

        return Response(
            {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "role_info": {
                    "role": user.role,
                    "application_status": user.application_status,
                    "application_role": user.application_role,
                },
                "message": "Registration successful. Please check your email to verify your account.",
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email_or_username, password=password)

        if not user:
            try:
                user_obj = User.objects.get(email=email_or_username)
                if user_obj.check_password(password):
                    user = user_obj
            except User.DoesNotExist:
                user = None

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)
        return Response(
            {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "role": user.role,
                **tokens,
            },
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email_or_username, password=password)

        if not user:
            try:
                user_obj = User.objects.get(email=email_or_username)
                if user_obj.check_password(password):
                    user = user_obj
            except User.DoesNotExist:
                user = None

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)
        return Response(
            {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "role_info": {
                    "role": user.role,
                    "application_status": user.application_status,
                    "application_role": user.application_role,
                },
                **tokens,
            },
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"{settings.FRONTEND_URL}/reset-password/?uid={uidb64}&token={token}"

        send_mail(
            subject="Reset your password",
            message=f"Click here to reset your password: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get("uidb64")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        otp = EmailOTP.generate_otp()
        EmailOTP.objects.update_or_create(email=email, defaults={"otp": otp, "is_verified": False})

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is {otp}. It expires in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "id": str(user.id),
                "email": user.email,
                "role":{
                    "application_status": user.application_status,
                    "application_role": user.application_role

                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class ApplyForUpgradeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        requested_role = request.data.get("requested_role")

        if user.role != User.Role.CUSTOMER:
            return Response(
                {"error": f"You are already a {user.role}. Upgrade not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.application_status == User.ApplicationStatus.PENDING:
            return Response(
                {"error": "You already have a pending request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate requested role
        if requested_role not in [User.Role.INFLUENCER, User.Role.VENDOR]:
            return Response(
                {"error": "Invalid role requested. Only Influencer or Vendor allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if requested_role == User.Role.VENDOR:
            serializer = VendorApplicationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user.business_name = serializer.validated_data["business_name"]
            user.gov_id_number = serializer.validated_data["gov_id_number"]
            user.certificate = serializer.validated_data["certificate"]

        user.application_role = requested_role
        user.application_status = User.ApplicationStatus.PENDING
        user.save()

        send_mail(
            subject=f"New {requested_role} Upgrade Request",
            message=f"User {user.email} has applied to become a {requested_role}. Please review.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

        return Response(
            {"message": f"{requested_role} upgrade request submitted successfully."},
            status=status.HTTP_201_CREATED,
        )
class ApproveUpgradeView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if user.application_status != User.ApplicationStatus.PENDING:
            return Response({"error": "No pending request to approve."}, status=status.HTTP_400_BAD_REQUEST)

        user.role = user.application_role
        user.application_status = User.ApplicationStatus.APPROVED
        user.save()

        dashboard_url = f"{settings.FRONTEND_URL}/dashboard"
        if user.role == User.Role.VENDOR:
            dashboard_url = f"{settings.FRONTEND_URL}/vendor-dashboard"
        elif user.role == User.Role.INFLUENCER:
            dashboard_url = f"{settings.FRONTEND_URL}/blog"

        send_mail(
            subject="Upgrade Approved",
            message=f"Congratulations! Your upgrade to {user.role} has been approved. "
            f"You can now access your dashboard here: {dashboard_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response({"message": f"User upgraded to {user.role}.", "redirect_url": dashboard_url}, status=status.HTTP_200_OK)


class RejectUpgradeView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if user.application_status != User.ApplicationStatus.PENDING:
            return Response({"error": "No pending request to reject."}, status=status.HTTP_400_BAD_REQUEST)

        user.application_status = User.ApplicationStatus.REJECTED
        user.save()

        send_mail(
            subject="Upgrade Request Rejected",
            message=f"Sorry, your upgrade request for {user.application_role} was rejected by admin.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response({"message": "Upgrade request rejected."}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "You have been logged out successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import RegisterSerializer, UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
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
                "role": user.role,
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

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user =User.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        uidb65 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"{settings.FRONTEND_URL}/reset-password/?uid={uidb65}&token={token}"

        send_mail(
            subject="Reset your password",
            message=f"Click here to reset your password: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset successful."})
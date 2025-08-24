from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

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
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

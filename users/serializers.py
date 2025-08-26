from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "country"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "phone", "country", "password", "role"]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"default": User.Role.CUSTOMER}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            phone=validated_data.get("phone"),
            country=validated_data.get("country"),
            role=validated_data.get("role", User.Role.CUSTOMER),
            password=validated_data["password"],
        )
        user.save()
        return user
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email found.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uidb64"]))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uidb64": "Invalid UID"})

        token = attrs.get("token")
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid or expired token"})

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user

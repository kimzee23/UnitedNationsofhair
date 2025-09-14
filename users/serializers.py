import re
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from users.models import User
from users.otp_models import EmailOTP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "country"]


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone",
            "country",
            "password",
            "confirm_password",
            "role",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"default": User.Role.CUSTOMER},
        }

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords must match")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not re.search(r"\d", password):
            raise serializers.ValidationError("Password must contain at least one number")

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            phone=validated_data.get("phone"),
            country=validated_data.get("country"),
            role=User.Role.CUSTOMER,
            password=validated_data["password"],
        )
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

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one number")
        return value

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


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email found.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data["email"]
        otp = data["otp"]

        try:
            otp_obj = EmailOTP.objects.get(email=email, otp=otp)
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP expired")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User not found")

        data["user"] = user
        return data


class RoleUpgradeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "application_role", "application_status"]
        read_only_fields = ["application_status"]

    def validate_application_role(self, value):
        if value not in [User.Role.INFLUENCER, User.Role.VENDOR]:
            raise serializers.ValidationError("You can only apply for Influencer or Vendor.")
        return value

class VendorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["business_name", "gov_id_number", "certificate"]

    def validate(self, data):
        if not data.get("business_name"):
            raise serializers.ValidationError({"business_name": "Business name is required"})
        if not data.get("gov_id_number"):
            raise serializers.ValidationError({"gov_id_number": "Government ID number is required"})
        if not data.get("certificate"):
            raise serializers.ValidationError({"certificate": "Certificate is required"})
        return data

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "country"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "phone", "country", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        role = validated_data.get("role", User.Role.CUSTOMER)

        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],  # no .split() here
            phone=validated_data.get("phone"),
            country=validated_data.get("country"),
            role=role,
            password=validated_data.get("password"),
        )
        return user

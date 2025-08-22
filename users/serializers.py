from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'email','username','role', 'country', 'password' ]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email','username','role', 'country', 'password' ]
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'].split(),
            phone = validated_data.get('phone'),
            country = validated_data.get('country'),
            role = validated_data.get('role'),
            password = validated_data.get('password')
        )
        return user
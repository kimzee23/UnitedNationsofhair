from rest_framework import serializers

from salons.models import Salon, Stylist, Region
from users.models import User



class SalonSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    region = serializers.SlugRelatedField(
        slug_field="country_code",
        queryset=Region.objects.all()
    )

    class Meta:
        model = Salon
        fields = [
            "id", "name", "owner", "description", "address",
            "city", "country", "phone", "website", "region"
        ]


class StylistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    salon_name = serializers.CharField(source="salon.name", read_only=True)

    class Meta:
        model = Stylist
        fields = [
            "id", "user", "salon", "salon_name",
            "specialization", "experience_level", "bio", "website"
        ]
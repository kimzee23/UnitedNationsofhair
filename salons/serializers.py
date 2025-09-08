from rest_framework import serializers

from salons.models import Salon, Stylist, Region
from users.models import User
from users.serializers import UserSerializer


class SalonSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())

    class Meta:
        model = Salon
        fields = ["id","name","owner", "description", "address",
                  "city", "country", "phone", 'website',"region"  ]


class StylistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    salon_name = serializers.CharField(source="salon.name", read_only=True)

    class Meta:
        model = Stylist
        fields = [ 'id','user', 'salon', 'salon_name','specialization',
                   'experience_level','bio',"website"]
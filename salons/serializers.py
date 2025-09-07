from rest_framework import serializers

from salons.models import Salon, Stylist
from users.serializers import UserSerializer


class SalonSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Salon
        fields = ["id","name","owner", "description", "address",
                  "city", "country", "phone", 'website'  ]
class StylistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    salon_name = serializers.CharField(source="salon.name", read_only=True)

    class Meta:
        model = Stylist
        fields = [ 'id','user', 'salon', 'salon_name','specialization',
                   'experience_level','bio',"website"]
from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "user", "business_name", "website", "rating"]
        read_only_fields = ["rating"]

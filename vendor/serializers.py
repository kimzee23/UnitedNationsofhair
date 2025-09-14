from rest_framework import serializers
from .models import VendorApplication

class VendorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorApplication
        fields = ["id", "business_name", "business_certificate", "national_id", "address", "phone", "status"]
        read_only_fields = ["status"]

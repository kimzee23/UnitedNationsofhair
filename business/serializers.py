from rest_framework import serializers

from business.models import Business


class BusinessSerializer(serializers.Serializer):
    class Meta:
        model = Business
        fields =["id", "name","email","phone","address","description","kyc_status","created_at","updated_at"]
        read_only_fields = ["kyc_status","created_at","updated_at"]
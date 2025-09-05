from rest_framework import serializers

from businesses.models import Business


class BusinessSerializer(serializers.Serializer):
    class Meta:
        model = Business
        fields =["id", "name","email","phone","address","description","kyc_status","created_at","updated_at"]
        read_only_fields = ["owner"]


    def create(self, validated_data):
        return Business.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
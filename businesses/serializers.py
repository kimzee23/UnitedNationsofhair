from rest_framework import serializers

from businesses.models import Business, Region


class BusinessSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(
        slug_field="country_code",
        queryset=Region.objects.all()
    )

    class Meta:
        model = Business
        fields =[
            "id", "name","email","phone","address","description",
                 "kyc_status","region","created_at","updated_at"
                 ]
        read_only_fields = ["owner"]


    def create(self, validated_data):
        return Business.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
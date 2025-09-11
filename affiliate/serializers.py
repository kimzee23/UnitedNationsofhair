from rest_framework import serializers
from .models import AffiliateLink, SponsoredListing, AdSlot

class AffiliateLinkSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = AffiliateLink
        fields = [
            "id",
            "product",
            "product_name",
            "user",
            "code",
            "clicks",
            "is_active",
        ]
        read_only_fields = ["clicks",  "user"]


class SponsoredListingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = SponsoredListing
        fields = [
            "id",
            "product",
            "product_name",
            "brand",
            "brand_name",
            "start_date",
            "end_date",
            "slot_position",
            "is_active",
        ]
        read_only_fields = ["is_active"]


class AdSlotSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    class Meta:
        model = AdSlot
        fields = [
            "id",
            "title",
            "brand",
            "brand_name",

            "image_url",
            "link",
            "slot_type",
            "start_date",
            "end_date",
            "is_active",
        ]
        read_only_fields = ["is_active"]

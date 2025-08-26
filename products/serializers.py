from rest_framework import serializers
from products.models import Brand, Category, Product
from users.models import User
from users.serializers import UserSerializer

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class BrandSerializer(serializers.ModelSerializer):
    owner =  UserSerializer(read_only=True)
    class Meta:
        model = Brand
        fields = ["id", "name", "description", "website", "country","owner"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    brand_id = serializers.UUIDField(write_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "price", "stock", "affiliate_url",
            "image_url", "image", "created_at", "updated_at",
            "brand", "category", "brand_id", "category_id",
        ]

    def create(self, validated_data):
        brand_id = validated_data.pop("brand_id")
        category_id = validated_data.pop("category_id", None)

        return Product.objects.create(
            **validated_data,
            brand_id=brand_id,
            category_id=category_id
        )

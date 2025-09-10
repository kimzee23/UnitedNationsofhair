from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from products.models import Brand, Category, Product, ProductCompare
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
        request = self.context.get("request")

        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            raise serializers.ValidationError({"brand_id": "Invalid brand_id. Brand does not exist."})

        if request.user != brand.owner and request.user.role != "SUPER_ADMIN":
            raise serializers.ValidationError({"brand_id": "You can only add products to your own brand."})

        if category_id:
            if not Category.objects.filter(id=category_id).exists():
                raise serializers.ValidationError({"category_id": "Invalid category_id. Category does not exist."})

        return Product.objects.create(
            **validated_data,
            brand=brand,
            category_id=category_id
        )

    def update(self, instance, validated_data):
        request = self.context.get("request")
        brand_id = validated_data.pop("brand_id", None)
        category_id = validated_data.pop("category_id", None)

        if request.user != instance.brand.owner.user and request.user.role != "SUPER_ADMIN":
            raise serializers.ValidationError({"permission": "You can only update your own products."})

        if brand_id:
            try:
                brand = Brand.objects.get(id=brand_id)
            except Brand.DoesNotExist:
                raise serializers.ValidationError({"brand_id": "Invalid brand_id."})

            if request.user != brand.owner.user and request.user.role != "SUPER_ADMIN":
                raise serializers.ValidationError({"brand_id": "You can only move products to your own brand."})
            instance.brand = brand


        if category_id:
            if not Category.objects.filter(id=category_id).exists():
                raise serializers.ValidationError({"category_id": "Invalid category_id."})
            instance.category_id = category_id

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProductCompareSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = ProductCompare
        fields = ["id", "products", "product_ids", "created_at"]

    def create(self, validated_data):
        products = validated_data.pop("product_ids")
        comparison = ProductCompare.objects.create(user=self.context["request"].user)
        comparison.products.set(products)

        return comparison

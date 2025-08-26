from rest_framework import serializers
from users.models import User
from influencers.models import Influencer, InfluencerProduct
from products.models import Product
from products.serializers import ProductSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class InfluencerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Influencer
        fields = ['id', 'user', 'user_id', 'bio', 'followers_count', 'social_links']
        read_only_fields = ['id']

    def validate_user_id(self, value):
        if not User.objects.filter(id=value, role="INFLUENCER").exists():
            raise serializers.ValidationError("User does not exist or is not an influencer")
        return value

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        return Influencer.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('user_id', None)
        return super().update(instance, validated_data)


class InfluencerProductSerializer(serializers.ModelSerializer):
    influencer_details = InfluencerSerializer(source='influencer', read_only=True)
    product_details = ProductSerializer(source='product', read_only=True)

    influencer = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    influencer_id = serializers.UUIDField(write_only=True)  # or IntegerField if PKs are integers
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = InfluencerProduct
        fields = [
            'id', 'influencer', 'influencer_details',
            'product', 'product_details',
            'influencer_id', 'product_id',
            'promote_url'
        ]
        read_only_fields = ['id', 'influencer', 'product']

    def validate(self, attrs):
        if InfluencerProduct.objects.filter(
                influencer_id=attrs.get('influencer_id'),
                product_id=attrs.get('product_id')
        ).exists():
            raise serializers.ValidationError("This influencer is already promoting this product")
        return attrs

    def create(self, validated_data):
        influencer_id = validated_data.pop('influencer_id')
        product_id = validated_data.pop('product_id')
        influencer = Influencer.objects.get(id=influencer_id)
        product = Product.objects.get(id=product_id)
        return InfluencerProduct.objects.create(influencer=influencer, product=product, **validated_data)

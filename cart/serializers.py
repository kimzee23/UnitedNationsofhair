from rest_framework import serializers
from cart.models import CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        return CartItem.objects.create(user=user, **validated_data)

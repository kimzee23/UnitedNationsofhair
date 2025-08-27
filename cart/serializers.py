from rest_framework import serializers

from cart.models import CartItem


class CartItemSerializer(serializers.Serializer):
    class Meta:
        model = CartItem
        fields = ["id", "user", "product", "quantity","added_at"]
        read_only_fields = ["id", "user", "added_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


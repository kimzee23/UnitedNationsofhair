from decimal import Decimal
from rest_framework import serializers
from django.db import transaction

from orders.models import Order, OrderItem, OrderStatus
from cart.models import CartItem



class OrderItemReadSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(source="product.id", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "product_name", "unit_price", "quantity", "subtotal"]


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "status", "total_amount",
            "shipping_full_name", "shipping_phone",
            "shipping_address_line1", "shipping_address_line2",
            "shipping_city", "shipping_state", "shipping_postal_code", "shipping_country",
            "payment_method", "payment_reference",
            "stock_deducted", "created_at", "updated_at", "items",
        ]


class CheckoutSerializer(serializers.ModelSerializer):
    """Create an order from the authenticated user's cart."""
    class Meta:
        model = Order
        fields = [
            "shipping_full_name", "shipping_phone",
            "shipping_address_line1", "shipping_address_line2",
            "shipping_city", "shipping_state", "shipping_postal_code", "shipping_country",
        ]

    def validate(self, attrs):
        user = self.context["request"].user
        cart_items = CartItem.objects.filter(user=user).select_related("product")
        if not cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        # Basic validations
        for ci in cart_items:
            if not ci.product.is_verified:
                raise serializers.ValidationError(
                    f"Product '{ci.product.name}' is not verified and cannot be ordered."
                )
            if ci.product.price is None:
                raise serializers.ValidationError(
                    f"Product '{ci.product.name}' does not have a price set."
                )
            if ci.quantity <= 0:
                raise serializers.ValidationError(
                    f"Invalid quantity for '{ci.product.name}'."
                )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        cart_items = (
            CartItem.objects.filter(user=user)
            .select_related("product")
            .select_for_update()
        )

        with transaction.atomic():
            # Compute total
            total = Decimal("0.00")
            for ci in cart_items:
                total += (ci.product.price * ci.quantity)

            order = Order.objects.create(
                user=user,
                status=OrderStatus.PENDING,
                total_amount=total,
                **validated_data,
            )

            # Snapshot items
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=ci.product,
                    product_name=ci.product.name,
                    unit_price=ci.product.price,
                    quantity=ci.quantity,
                    subtotal=(ci.product.price * ci.quantity),
                )
                for ci in cart_items
            ])

            # Clear cart
            cart_items.delete()

        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
        extra_kwargs = {"status": {"required": True}}

    def validate_status(self, value):
        allowed = {OrderStatus.PENDING, OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED}
        if value not in allowed:
            raise serializers.ValidationError("Invalid status.")
        return value

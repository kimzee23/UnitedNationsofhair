
import uuid
from decimal import Decimal
from django.db import models, transaction
from django.conf import settings

from products.models import Product
User = settings.AUTH_USER_MODEL


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "pending"
    PAID = "PAID", "paid"
    SHIPPED = "SHIPPED", "shipped"
    DELIVERED = "DELIVERED", "delivered"
    CANCELLED = "CANCELLED", "cancelled"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    # Shipping snapshot
    shipping_full_name = models.CharField(max_length=150)
    shipping_phone = models.CharField(max_length=30, blank=True, null=True)
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=30)
    shipping_country = models.CharField(max_length=100)

    # Payment snapshot (dummy)
    payment_method = models.CharField(max_length=50, blank=True, null=True)   # e.g. "STRIPE", "DUMMY"
    payment_reference = models.CharField(max_length=200, blank=True, null=True)

    # Guard so we only deduct stock once
    stock_deducted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")

    # Snapshots for history
    product_name = models.CharField(max_length=400)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product_name} x{self.quantity}"

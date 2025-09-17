import uuid
from django.db import models
from django.conf import settings
from orders.models import Order


class PaymentProvider(models.TextChoices):
    PAYSTACK = "PAYSTACK", "Paystack"
    PAYPAL = "PAYPAL", "PayPal"


class PaymentStatus(models.TextChoices):
    INITIATED = "INITIATED", "Initiated"
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    provider = models.CharField(max_length=20, choices=PaymentProvider.choices)
    reference = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.INITIATED)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider} {self.reference} - {self.status} for Order {self.order.id}"

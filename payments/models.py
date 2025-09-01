from django.db import models
import uuid
from django.db import models
from django.conf import settings
from orders.models import Order

class PaymentProvider(models.TextChoices):
    PAYSTACK = "PAYSTACK", "Paystack"
    OPAY = "OPAY", "Opay"
    CUSTOM = "CUSTOM", "Custom"
    DUMMY = "DUMMY", "Dummy"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    provider = models.CharField(max_length=20, choices=PaymentProvider.choices)
    reference = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default="INITIATED")  # INITIATED, SUCCESS, FAILED
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider} {self.reference} - {self.status}payment for {self.order.id}"

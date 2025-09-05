import uuid

from django.conf import settings
from django.db import models

class Business(models.Model):
    class KYCStatus(models.TextChoices):
        PENDING = "PENDING","pending"
        APPROVED = "APPROVED","approved"
        REJECTED = "REJECTED","rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(
          settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business"
       )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    description = models.TextField(blank=True)
    kyc_status = models.CharField(
        max_length=20, choices=KYCStatus.choices, default=KYCStatus.PENDING
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

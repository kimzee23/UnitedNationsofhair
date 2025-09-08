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
          settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="businesses"
       )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    description = models.TextField(blank=True)
    kyc_status = models.CharField(
        max_length=20, choices=KYCStatus.choices, default=KYCStatus.PENDING
        )
    region = models.ForeignKey(
        "Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="businesses"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Region(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5)
    currency = models.CharField(max_length=10, default="USD")
    language = models.CharField(max_length=20, default="en")

    def __str__(self):
        return self.name

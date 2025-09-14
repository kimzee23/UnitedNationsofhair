import uuid
from django.db import models
from django.conf import settings

class VendorApplication(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendor_application")

    business_name = models.CharField(max_length=255)
    business_certificate = models.FileField(upload_to="vendors/certificates/")
    national_id = models.FileField(upload_to="vendors/national_ids/")
    address = models.TextField()
    phone = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.business_name} ({self.status})"

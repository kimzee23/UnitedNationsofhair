import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "super admin"
        VENDOR = "VENDOR", "vendor"
        INFLUENCER = "INFLUENCER", "influencer"
        CUSTOMER = "CUSTOMER", "customer"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,
                            choices=Role.choices, default=Role.CUSTOMER, editable=False)
    country = models.CharField(max_length=100, blank=True,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email" , "phone"]

    def __str__(self):
        return f"{self.username} ({self.role})"



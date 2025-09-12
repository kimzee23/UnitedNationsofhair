import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, phone=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone=None, password=None, **extra_fields):

        extra_fields.setdefault("role", User.Role.SUPER_ADMIN)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        return self.create_user(email, username, phone, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "super admin"
        VENDOR = "VENDOR", "vendor"
        INFLUENCER = "INFLUENCER", "influencer"
        CUSTOMER = "CUSTOMER", "customer"

    class ApplicationStatus(models.TextChoices):
        NONE = "NONE", "none"
        PENDING = "PENDING", "pending"
        APPROVED = "APPROVED", "approved"
        REJECTED = "REJECTED", "rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.CUSTOMER, editable=False
    )
    country = models.CharField(max_length=100, blank=True, null=True)

    application_role = models.CharField(
        max_length=20, choices=Role.choices, null=True, blank=True
    )
    application_status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices,
        default=ApplicationStatus.NONE
    )

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.Role.SUPER_ADMIN
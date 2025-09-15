import random
from django.db import models
from django.utils import timezone


class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300

    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))

from django.db import models


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
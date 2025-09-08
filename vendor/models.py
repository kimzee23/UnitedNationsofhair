#
from django.db import models
from users.models import User

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_profile")
    business_name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name or self.user.username

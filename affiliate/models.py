import uuid
from django.db import models
from django.utils import timezone
from products.models import Product, Brand
from users.models import User


class AffiliateLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="affiliate_links")
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="affiliate_links")
    code = models.CharField(max_length=50, unique=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def increment_clicks(self):
        # Update DB and instance
        from django.db.models import F
        AffiliateLink.objects.filter(id=self.id).update(clicks=F('clicks') + 1)
        self.refresh_from_db(fields=['clicks'])

    def __str__(self):
        return f"{self.product.name} - {self.user.username if self.user else 'Anonymous'}"


class SponsoredListing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sponsored_listings")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="sponsored_listings")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slot_position = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('slot_position', 'brand')

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.is_active = self.start_date <= now <= self.end_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} sponsored by {self.brand.name}"


class AdSlot(models.Model):
    SLOT_TYPES = [
        ("banner", "Banner"),
        ("sidebar", "Sidebar"),
        ("popup", "Popup"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="ad_slots")
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="ads/")
    link = models.URLField()
    slot_type = models.CharField(max_length=20, choices=SLOT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.is_active = self.start_date <= now <= self.end_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.brand.name})"

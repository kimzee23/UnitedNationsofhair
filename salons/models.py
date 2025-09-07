import uuid

from django.db import models
from django.utils import timezone

from users.models import User


class Salon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="salons")
    description = models.CharField(blank=True, null=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=250)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    website = models.URLField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ("name", "city", "country")
    def __str__(self):
        return f"{self.name} ({self.city}), {self.country}"

class Stylist(models.Model):
    STYLIST_EXPERIENCE_CHOICES = [
        (1, '1-2 years (Emerging Stylist)'),
        (2, '2-4 years (Skilled Stylist)'),
        (4, '4-7 years (Senior Stylist)'),
        (7, '7-8 years (Master Stylist)'),
        (9, '9-12 years (Artistic Director Level)'),
        (12, '12-15 years (Creative Director)'),
        (15, '16+ years (Industry Icon)'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stylist_profile")
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="stylist_salon")
    bio = models.TextField(blank=True, null=True)
    specialization = models.CharField()
    experience_level = models.PositiveIntegerField(choices=STYLIST_EXPERIENCE_CHOICES,default=0)
    website = models.URLField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialization or 'Stylist'} ({self.salon.name})"
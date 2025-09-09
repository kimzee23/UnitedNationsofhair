import uuid

from django.db import models

from users.models import User


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "VENDOR"}
    )

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=400)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    stock = models.IntegerField(default=0)
    affiliate_url = models.URLField(blank=True,null=True)
    image_url = models.URLField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")

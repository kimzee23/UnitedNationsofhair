import uuid

from django.db import models

from products.models import Product
from users.models import User


class WishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")
    added_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ('user', 'product')

def __str__(self):
    return f"{self.user.username} - {self.product.name}"

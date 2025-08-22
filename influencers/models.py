import uuid

from django.db import models

from products.models import Product
from users.models import User


class Influencer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio =models.TextField(blank=True)
    followers_count = models.IntegerField(default=0)
    social_links = models.JSONField(default=dict,blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': "INFLUENCER"})

    def __str__(self):
        return f"Influencer {self.user.username}"

class InfluencerProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE, related_name='promoted_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='promoted_by')
    promote_url = models.URLField(blank=True,null=True)

    class Meta:
        unique_together = ('influencer', 'product')

    def __str__(self):
        return f"{self.influencer.user.username}  promotes {self.product.name}"
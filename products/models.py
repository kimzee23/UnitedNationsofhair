import uuid

from django.db import models


class Brands(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)


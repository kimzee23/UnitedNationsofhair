import uuid

from django.contrib.auth import get_user_model
from django.db import models

from users.models import User

user = get_user_model()

class Tutorial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(help_text="Step by step guide or article")
    video = models.FileField(upload_to="tutorials/videos/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="tutorials/thumbnails/", blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tutorials")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} n/ {self.description}"

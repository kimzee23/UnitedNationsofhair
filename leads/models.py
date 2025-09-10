from django.db import models

from users.models import User


class Lead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    interest = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead {self.name} ({self.email})"
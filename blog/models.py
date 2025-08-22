from django.db import models

from users.models import User


class BlogArticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()

    hero_image_url = models.URLField(blank=True,null=True)
    hero_image = models.ImageField(upload_to="blogs/", blank=True,null=True)

    tags = models.JSONField(default=list, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey("users.User", on_delete=models.CASCADE, limit_choices_to={'role_in': ["INFLUENCER", "SUPER_ADMIN"]})

    def __str__(self):
        return f'new post, {self.title}'
from django.db import models
from django.utils import timezone
from video_encoding.fields import VideoField

class BlogArticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()

    hero_image_url = models.URLField(blank=True, null=True)
    hero_image = VideoField(upload_to="blogs/", blank=True, null=True)

    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to="blogs/videos/", blank=True, null=True)

    tags = models.JSONField(default=list, null=True)

    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ["INFLUENCER", "SUPER_ADMIN"]}
    )
    excerpt = models.TextField(max_length=300, blank=True, null=True)
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.CharField(max_length=160, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f'new post, {self.title}'

    def publish(self):
        self.is_published = True
        if not self.published_at:
            self.published_at = timezone.now()
        self.save()

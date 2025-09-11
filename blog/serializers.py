from django.template.context_processors import request
from django.utils.text import slugify
from rest_framework import serializers

from blog.models import BlogArticle


class BlogArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = BlogArticle
        fields = [
            "uuid", "title", "slug", "body",
            "excerpt", "seo_title", "seo_description",
            "is_published", "views","published_at",
            "hero_image_url", "hero_image", "tags",
            "created_at", "updated_at","video_url", "video_file",
            "author", "author_name"
        ]
        read_only_fields = ["author", "created_at", "updated_at", "views"]



    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["title"])
        return super().create(validated_data)
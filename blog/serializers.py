from django.template.context_processors import request
from rest_framework import serializers

from blog.models import BlogArticle


class BlogArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    class Meta:
        model = BlogArticle
        fields = [
            "id",
            "title",
            "slug",
            "body",
            "hero_image_url",
            "hero_image",
            "tags",
            "created_at",
            "updated_at",
            "author",
            "author_name"
        ]
        read_only_fields = ["author","created_at", "updated_at"]

    def create(self, validated_data):
        request  = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)

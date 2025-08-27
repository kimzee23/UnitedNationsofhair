from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "created_at", "user", "product"]
        read_only_fields = ["id", "created_at", "user"]
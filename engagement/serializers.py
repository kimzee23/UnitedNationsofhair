from rest_framework import serializers
from .models import Comment, Like, Follow


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "content_type", "object_id")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "content_type", "object_id")

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ("id", "follower", "created_at")

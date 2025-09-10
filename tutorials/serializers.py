from rest_framework import serializers
from .models import Tutorial

class TutorialSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Tutorial
        fields = [
            "id", "title", "description", "content", "video",
            "thumbnail", "created_by", "created_by_name",
            "is_published"
        ]
        read_only_fields = ["created_by", "created_by_name"]

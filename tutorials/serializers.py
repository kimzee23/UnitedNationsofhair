from rest_framework import serializers

from tutorials.models import Tutorial


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ["id", "title", "description", "video",
                  "thumbnail", "created_by", "created_by_name",
                  "is_published"
                  ]
        read_only_fields = ["created_at","created_by_name","created_at","updated_at"]
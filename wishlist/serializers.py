from rest_framework import serializers

from wishlist.models import WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["id", "user","product","added_at"]
        read_only_fields = ["id","user","added_at"]
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Comment, Like, Follow
from .serializers import CommentSerializer, LikeSerializer, FollowSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            content_type=self.kwargs["content_type"],
            object_id=self.kwargs["object_id"]
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeToggleView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        like, created = Like.objects.get_or_create(
            user=self.request.user,
            content_type=self.kwargs["content_type"],
            object_id=self.kwargs["object_id"]
        )
        if not created:  # If already liked → unlike
            like.delete()


class FollowToggleView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        follow, created = Follow.objects.get_or_create(
            follower=self.request.user,
            following_id=self.kwargs["user_id"]
        )
        if not created:  # If already following → unfollow
            follow.delete()

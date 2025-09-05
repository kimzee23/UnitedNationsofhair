from rest_framework import generics, permissions, status
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Like, Follow
from .serializers import CommentSerializer, LikeSerializer, FollowSerializer
from blog.models import BlogArticle
from products.models import Product

User = get_user_model()


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        model = self._get_model()
        content_type = ContentType.objects.get_for_model(model)
        return Comment.objects.filter(
            content_type=content_type,
            object_id=self.kwargs["object_id"]
        )

    def perform_create(self, serializer):
        model = self._get_model()
        content_type = ContentType.objects.get_for_model(model)
        serializer.save(
            user=self.request.user,
            content_type=content_type,
            object_id=self.kwargs["object_id"]
        )

    def _get_model(self):
        if "blog" in self.request.path:
            return BlogArticle
        elif "product" in self.request.path:
            return Product


class LikeToggleView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        object_id = self.kwargs["object_id"]

        if "blog" in self.request.path:
            content_type = "blog"
        else:
            content_type = "product"

        like, created = Like.objects.get_or_create(
            user=self.request.user,
            content_type=content_type,
            object_id=object_id
        )
        if not created:
            like.delete()


class FollowToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        target_user = User.objects.get(id=self.kwargs["user_id"])
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )
        if not created:
            follow.delete()
        return Response({"success": True}, status=status.HTTP_201_CREATED)
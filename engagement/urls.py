from django.urls import path
from .views import CommentListCreateView, LikeToggleView, FollowToggleView

urlpatterns = [
    # Blog endpoints (int IDs)
    path("blog/<int:object_id>/comments/", CommentListCreateView.as_view(), name="blog-comments"),
    path("blog/<int:object_id>/like/", LikeToggleView.as_view(), name="blog-like-toggle"),

    # Product endpoints (UUID IDs, adjust if Product uses int instead)
    path("product/<uuid:object_id>/comments/", CommentListCreateView.as_view(), name="product-comments"),
    path("product/<uuid:object_id>/like/", LikeToggleView.as_view(), name="product-like-toggle"),

    # Follow (User IDs are UUIDs)
    path("follow/<uuid:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),
]

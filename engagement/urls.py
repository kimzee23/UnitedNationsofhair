from django.urls import path
from .views import CommentListCreateView, LikeToggleView, FollowToggleView

urlpatterns = [
    # Comments
    path("<str:content_type>/<uuid:object_id>/comments/", CommentListCreateView.as_view(), name="comments"),

    # Likes
    path("<str:content_type>/<uuid:object_id>/like/", LikeToggleView.as_view(), name="like-toggle"),

    # Follows
    path("follow/<uuid:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),
]

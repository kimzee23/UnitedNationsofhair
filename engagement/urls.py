from django.urls import path
from .views import CommentListCreateView, LikeToggleView, FollowToggleView

urlpatterns = [

    path("blog/<int:object_id>/comments/", CommentListCreateView.as_view(), name="blog-comments"),
    path("blog/<int:object_id>/like/", LikeToggleView.as_view(), name="blog-like-toggle"),

    path("product/<uuid:object_id>/comments/", CommentListCreateView.as_view(), name="product-comments"),
    path("product/<uuid:object_id>/like/", LikeToggleView.as_view(), name="product-like-toggle"),

    path("follow/<uuid:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),

]


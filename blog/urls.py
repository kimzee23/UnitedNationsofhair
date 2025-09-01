from django.urls import path
from blog.views import BlogArticleListCreateView, BlogArticleDetailView

urlpatterns = [
    path("blog", BlogArticleListCreateView.as_view(), name="blog-list-create"),
    path("<int:pk>/", BlogArticleDetailView.as_view(), name="blog-detail"),
]

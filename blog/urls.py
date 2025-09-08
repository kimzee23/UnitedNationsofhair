from django.urls import path
from blog.views import BlogArticleListCreateView, BlogArticleDetailView, PublicBlogListView, PublicBlogDetailView

urlpatterns = [
    path("blog/", BlogArticleListCreateView.as_view(), name="blog-list-create"),
    path("<int:pk>/", BlogArticleDetailView.as_view(), name="blog-detail"),
    path("public/", PublicBlogListView.as_view(), name="public-blog-list"),
    path("public/<slug:slug>/", PublicBlogDetailView.as_view(), name="public-blog-detail"),

]

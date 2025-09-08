from rest_framework import generics, permissions
from blog.models import BlogArticle
from blog.permissions import IsInfluencerOrAdmin
from blog.serializers import BlogArticleSerializer


class BlogArticleListCreateView(generics.ListCreateAPIView):
    queryset = BlogArticle.objects.all().order_by("-created_at")
    serializer_class = BlogArticleSerializer
    permission_classes = [IsInfluencerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogArticle.objects.all()
    serializer_class = BlogArticleSerializer
    permission_classes = [IsInfluencerOrAdmin]


class PublicBlogListView(generics.ListAPIView):
    queryset = BlogArticle.objects.filter(is_published=True).order_by("-created_at")
    serializer_class = BlogArticleSerializer
    permission_classes = [permissions.AllowAny]


class PublicBlogDetailView(generics.RetrieveAPIView):
    queryset = BlogArticle.objects.filter(is_published=True).order_by("-created_at")
    serializer_class = BlogArticleSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save(update_fields=["views"])
        return obj

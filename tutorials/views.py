from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Tutorial
from .serializers import TutorialSerializer

class IsInfluencer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "INFLUENCER"

class TutorialListCreateView(generics.ListCreateAPIView):
    queryset = Tutorial.objects.filter(is_published=True)
    serializer_class = TutorialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsInfluencer()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TutorialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

class PublicTutorialListView(generics.ListAPIView):
    queryset = Tutorial.objects.filter(is_published=True)
    serializer_class = TutorialSerializer
    permission_classes = [permissions.AllowAny]

class PublicTutorialDetailView(generics.RetrieveAPIView):
    queryset = Tutorial.objects.filter(is_published=True)
    serializer_class = TutorialSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=["views"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

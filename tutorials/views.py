from rest_framework import generics, permissions

from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer


class TutorialListCreateView(generics.ListCreateAPIView):
    queryset = Tutorial.objects.filter(is_published=True)
    serializer_class = TutorialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TutorialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)
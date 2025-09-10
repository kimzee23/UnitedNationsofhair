from rest_framework import generics, permissions, serializers

from leads.models import Lead
from leads.serializers import LeadSerializer


class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError({"user": "User is required"})


class LeadListView(generics.ListAPIView):
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer
    permission_classes = [permissions.AllowAny]




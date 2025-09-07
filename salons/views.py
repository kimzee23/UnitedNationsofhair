from rest_framework import generics, permissions

from salons.models import Salon, Stylist
from salons.serializers import SalonSerializer, StylistSerializer
from users.permissions import IsVendorOrAdmin


class SalonListCreateView(generics.ListCreateAPIView):
    serializer_class = SalonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPER_ADMIN':
            return Salon.objects.all()
        return Salon.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SalonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SalonSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPER_ADMIN':
            return Salon.objects.all()
        return Salon.objects.filter(owner=user)

class StylistListCreateView(generics.ListCreateAPIView):
    serializer_class = StylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return Stylist.objects.all()
        return Stylist.objects.filter(salon__owner=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return Stylist.objects.all()
        return Stylist.objects.filter(salon__owner=user)
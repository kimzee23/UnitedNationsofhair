from rest_framework import generics, permissions, serializers

from salons.models import Salon, Stylist, Region
from salons.serializers import SalonSerializer, StylistSerializer
from users.models import User
from users.permissions import IsVendorOrAdmin


class SalonListCreateView(generics.ListCreateAPIView):
    serializer_class = SalonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        region_code = self.request.query_params.get("region")  # filter by region
        qs = Salon.objects.all() if user.role == 'SUPER_ADMIN' else Salon.objects.filter(owner=user)
        if region_code:
            qs = qs.filter(region__country_code__iexact=region_code)
        return qs

    def perform_create(self, serializer):
        region_id = self.request.data.get("region")
        region = None
        if region_id:
            try:
                region = Region.objects.get(id=region_id)
            except Region.DoesNotExist:
                raise serializers.ValidationError({"region": "Region does not exist"})
        serializer.save(owner=self.request.user, region=region)


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
        user_id = self.request.data.get("user")
        user = User.objects.get(id=user_id)
        salon_id = self.request.data.get("salon")
        salon = Salon.objects.get(id=salon_id)
        serializer.save(user=user, salon=salon)

class StylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return Stylist.objects.all()
        return Stylist.objects.filter(salon__owner=user)
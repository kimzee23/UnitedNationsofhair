from rest_framework import generics, permissions, serializers
from django.shortcuts import get_object_or_404

from salons.models import Salon, Stylist, Region
from salons.serializers import SalonSerializer, StylistSerializer
from users.models import User
from users.permissions import IsVendorOrAdmin


class SalonListCreateView(generics.ListCreateAPIView):
    serializer_class = SalonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        region_code = self.request.query_params.get("region")
        qs = Salon.objects.all() if user.role == 'SUPER_ADMIN' else Salon.objects.filter(owner=user)
        if region_code:
            qs = qs.filter(region__country_code__iexact=region_code)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SalonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SalonSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return Salon.objects.all() if user.role == 'SUPER_ADMIN' else Salon.objects.filter(owner=user)


class StylistListCreateView(generics.ListCreateAPIView):
    serializer_class = StylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return Stylist.objects.all() if user.role == "SUPER_ADMIN" else Stylist.objects.filter(salon__owner=user)

    def perform_create(self, serializer):
        user = get_object_or_404(User, id=self.request.data.get("user"))
        salon = get_object_or_404(Salon, id=self.request.data.get("salon"))
        serializer.save(user=user, salon=salon)


class StylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return Stylist.objects.all() if user.role == "SUPER_ADMIN" else Stylist.objects.filter(salon__owner=user)

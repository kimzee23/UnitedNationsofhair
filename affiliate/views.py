from rest_framework import generics, permissions, status
from rest_framework.response import Response
from affiliate.models import AffiliateLink, SponsoredListing, AdSlot
from affiliate.permissions import IsVendorOrAdminOrInfluencer
from affiliate.serializers import AffiliateLinkSerializer, SponsoredListingSerializer, AdSlotSerializer
from users.permissions import IsVendorOrAdmin



class AffiliateLinkListCreateView(generics.ListCreateAPIView):
    serializer_class = AffiliateLinkSerializer
    permission_classes = [IsVendorOrAdminOrInfluencer]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return AffiliateLink.objects.all()
        return AffiliateLink.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AffiliateLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AffiliateLinkSerializer
    permission_classes = [IsVendorOrAdminOrInfluencer]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return AffiliateLink.objects.all()
        return AffiliateLink.objects.filter(user=user)



class SponsoredListingListCreateView(generics.ListCreateAPIView):
    serializer_class = SponsoredListingSerializer
    permission_classes = [IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return SponsoredListing.objects.all()
        return SponsoredListing.objects.filter(brand__owner=user)


class SponsoredListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SponsoredListingSerializer
    permission_classes = [IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return SponsoredListing.objects.all()
        return SponsoredListing.objects.filter(brand__owner=user)



class AdSlotListCreateView(generics.ListCreateAPIView):
    serializer_class = AdSlotSerializer
    permission_classes = [IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return AdSlot.objects.all()
        return AdSlot.objects.filter(brand__owner=user)


class AdSlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdSlotSerializer
    permission_classes = [IsVendorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPER_ADMIN":
            return AdSlot.objects.all()
        return AdSlot.objects.filter(brand__owner=user)

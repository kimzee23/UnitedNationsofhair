from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Vendor
from .serializers import VendorSerializer
from users.models import User

class VendorListCreateView(generics.ListCreateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.SUPER_ADMIN:
            return Vendor.objects.all()
        # Regular users only see their own vendor profile
        return Vendor.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Retrieve / Update vendor profile for the logged-in user
class VendorDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Assumes a one-to-one relation: User → Vendor
        return get_object_or_404(Vendor, user=self.request.user)


# Approve a vendor application (Admin only)
class ApproveVendorView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        user = vendor.user

        if user.application_status != User.ApplicationStatus.PENDING:
            return Response({"error": "No pending request to approve."}, status=status.HTTP_400_BAD_REQUEST)

        user.role = User.Role.VENDOR
        user.application_status = User.ApplicationStatus.APPROVED
        user.save()

        return Response({"message": f"{user.username} is now a vendor."}, status=status.HTTP_200_OK)


# Reject a vendor application (Admin only)
class RejectVendorView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        user = vendor.user

        if user.application_status != User.ApplicationStatus.PENDING:
            return Response({"error": "No pending request to reject."}, status=status.HTTP_400_BAD_REQUEST)

        user.application_status = User.ApplicationStatus.REJECTED
        user.save()

        return Response({"message": f"{user.username}'s vendor request has been rejected."}, status=status.HTTP_200_OK)

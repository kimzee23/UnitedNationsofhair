from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from businesses.models import Business
from businesses.serializers import BusinessSerializer
from users.permissions import IsAdmin


class BusinessApplyView(generics.CreateAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        region_code = self.request.query_params.get("region")
        qs = Business.objects.all() if user.role == 'SUPER_ADMIN' else Business.objects.filter(owner=user)
        if region_code:
            qs = qs.filter(region__country_code__iexact=region_code)
        return qs

    def perform_create(self, serializer):
        if Business.objects.filter(owner=self.request.user).exists():
            raise ValidationError({"detail": "You already have a business."})
        business = serializer.save(owner=self.request.user)

        if business.region and business.region.country_code in ["NG", "US"]:
            business.kyc_status = Business.KYCStatus.APPROVED
            business.save(update_fields=["kyc_status"])

class BusinessDashboardView(generics.RetrieveAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return Business.objects.get(owner=self.request.user)
        except Business.DoesNotExist:
            raise NotFound("No business found for this user.")

class BusinessApproveView(generics.UpdateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        business = self.get_object()
        if business.kyc_status != Business.KYCStatus.PENDING:
            return Response({"detail": "Already processed"}, status=status.HTTP_400_BAD_REQUEST)

        business.kyc_status = Business.KYCStatus.APPROVED
        business.save(update_fields=["kyc_status"])
        serializer = self.get_serializer(business)
        return Response(serializer.data)

class BusinessRejectView(generics.UpdateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        business = self.get_object()
        if business.kyc_status != Business.KYCStatus.PENDING:
            return Response({"detail": "Already processed"}, status=status.HTTP_400_BAD_REQUEST)

        business.kyc_status = Business.KYCStatus.REJECTED
        business.save(update_fields=["kyc_status"])
        serializer = self.get_serializer(business)
        return Response(serializer.data)
class BusinessListView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        region = self.request.query_params.get("region")
        country = Business.objects.filter(kyc_status=Business.KYCStatus.APPROVED)
        if region:
            country = country.filter(region__country_code__iexact=region)
        return country

class BusinessBulkApproveView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        ids = request.data.get("business_ids", [])
        if not ids:
            return Response({"detail": "No business IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Business.objects.filter(id__in=ids, kyc_status=Business.KYCStatus.PENDING)
        count = queryset.update(kyc_status=Business.KYCStatus.APPROVED)
        return Response({"approved_count": count}, status=status.HTTP_200_OK)


class BusinessBulkRejectView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        ids = request.data.get("business_ids", [])
        if not ids:
            return Response({"detail": "No business IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Business.objects.filter(id__in=ids, kyc_status=Business.KYCStatus.PENDING)
        count = queryset.update(kyc_status=Business.KYCStatus.REJECTED)
        return Response({"rejected_count": count}, status=status.HTTP_200_OK)
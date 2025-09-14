from django.urls import path
from .views import VendorApplicationCreateView, VendorApplicationApproveView

urlpatterns = [
    path("vendor/apply/", VendorApplicationCreateView.as_view(), name="vendor-apply"),
    path("vendor/<uuid:pk>/review/", VendorApplicationApproveView.as_view(), name="vendor-review"),
]

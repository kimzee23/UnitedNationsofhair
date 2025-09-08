from django.urls import path
from vendor import views
from vendor.views import VendorListCreateView, VendorDetailView

urlpatterns = [

    path("", VendorListCreateView.as_view(), name="vendor-list-create"),
    path("me/", VendorDetailView.as_view(), name="vendor-detail"),

    path("<uuid:pk>/approve/", views.ApproveVendorView.as_view(), name="vendor-approve"),
    path("<uuid:pk>/reject/", views.RejectVendorView.as_view(), name="vendor-reject"),
]

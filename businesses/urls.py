from django.urls import path
from .views import BusinessApplyView, BusinessDashboardView, BusinessApproveView, BusinessRejectView

urlpatterns = [
    path("apply/", BusinessApplyView.as_view(), name="business-apply"),
    path("dashboard/", BusinessDashboardView.as_view(), name="business-dashboard"),
    path("<uuid:pk>/approve/", BusinessApproveView.as_view(), name="business-approve"),
    path("<uuid:pk>/reject/", BusinessRejectView.as_view(), name="business-reject"),
]
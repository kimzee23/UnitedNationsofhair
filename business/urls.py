from django.urls import path

from business.views import BusinessApplyView, BusinessDashboardView, BusinessApprovalView

urlpatterns = [
    path("apply/", BusinessApplyView.as_view(), name="business-apply"),
    path("dashboard/", BusinessDashboardView.as_view(), name="business-dashboard"),
    path("<uuid:pk>/approve/", BusinessApprovalView.as_view(), name="business-approve"),
]
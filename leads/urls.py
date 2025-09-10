from django.urls import path

from leads.views import LeadCreateView, LeadListView

urlpatterns = [
    path("leads/", LeadCreateView.as_view(), name="lead-create"),
    path("leads/all", LeadListView.as_view(), name="lead-list"),
]
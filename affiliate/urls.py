from django.urls import path
from .views import (
    AffiliateLinkListCreateView,
    AffiliateLinkDetailView,
    SponsoredListingListCreateView,
    SponsoredListingDetailView,
    AdSlotListCreateView,
    AdSlotDetailView,
)

urlpatterns = [
    path("links/", AffiliateLinkListCreateView.as_view(), name="affiliate-link-list-create"),
    path("links/<uuid:pk>/", AffiliateLinkDetailView.as_view(), name="affiliate-link-detail"),

    path("sponsored/", SponsoredListingListCreateView.as_view(), name="sponsored-listing-list-create"),
    path("sponsored/<uuid:pk>/", SponsoredListingDetailView.as_view(), name="sponsored-listing-detail"),

    path("ad-slots/", AdSlotListCreateView.as_view(), name="ad-slot-list-create"),
    path("ad-slots/<uuid:pk>/", AdSlotDetailView.as_view(), name="ad-slot-detail"),
]

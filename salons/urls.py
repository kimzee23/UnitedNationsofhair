from django.urls import path

from salons.views import SalonListCreateView, SalonDetailView, StylistListCreateView, StylistDetailView

urlpatterns = [
    path("salons/", SalonListCreateView.as_view(), name="salons-list-create"),
    path("salons/<uuid:pk>", SalonDetailView.as_view(), name="salons-detail"),
    path("stylists/", StylistListCreateView.as_view(), name="stylists-list-create"),
    path("stylists/<uuid:pk>/", StylistDetailView.as_view(), name="stylists-detail"),

]
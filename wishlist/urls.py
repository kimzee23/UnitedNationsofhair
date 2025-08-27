from django.urls import path

from wishlist.views import WishlistItemListCreateView, WishlistItemDeleteView

urlpatterns = [
    path("", WishlistItemListCreateView.as_view(), name="wishlist-list-create"),
    path("<uuid:pk>/", WishlistItemDeleteView.as_view(), name="wishlist-delete"),
]
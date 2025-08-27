from django.urls import path

from cart.views import CartItemListCreateView, CartItemDeleteView

urlpatterns = [
    path("",CartItemListCreateView.as_view(), name="cart-list-create"),
    path("<uuid:pk>/", CartItemDeleteView.as_view(), name="cart-delete"),
]
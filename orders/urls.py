from django.urls import path

from orders.views import CheckoutView, MyOrdersListView, AdminAllOrdersListView, OrderDetailView, PayOrderDummyView, \
    AdminOrderStatusUpdateView

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", MyOrdersListView.as_view(), name="my-orders"),
    path("all/", AdminAllOrdersListView.as_view(), name="admin-orders"),
    path("<uuid:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<uuid:pk>/pay/", PayOrderDummyView.as_view(), name="order-pay"),
    path("<uuid:pk>/status/", AdminOrderStatusUpdateView.as_view(), name="order-status"),
]
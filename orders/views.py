from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from orders.models import Order, OrderStatus
from orders.permissions import IsOwnerOrAdmin
from orders.serializers import (
    CheckoutSerializer, OrderDetailSerializer, OrderStatusUpdateSerializer
)


class CheckoutView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save()   # return the created order

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)   # only call once
        out = OrderDetailSerializer(order).data
        return Response(out, status=status.HTTP_201_CREATED)



class MyOrdersListView(generics.ListAPIView):
    """
    GET /api/v1/orders/
    List orders for the authenticated user.
    Admins can see all using /api/v1/orders/all/
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class AdminAllOrdersListView(generics.ListAPIView):
    """
    GET /api/v1/orders/all/
    Admin-only list of all orders.
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all().order_by("-created_at")


class OrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/orders/<uuid:pk>/
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [IsOwnerOrAdmin]
    queryset = Order.objects.all()


class PayOrderDummyView(APIView):
    """
    PATCH /api/v1/orders/<uuid:pk>/pay/
    Dummy payment to mark an order as PAID.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        # Only owner or admin can pay this order
        if not (request.user.is_staff or order.user_id == request.user.id):
            return Response({"detail": "Not permitted."}, status=status.HTTP_403_FORBIDDEN)

        if order.status != OrderStatus.PENDING:
            return Response({"detail": f"Order is already {order.status}."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = OrderStatus.PAID
        order.payment_method = "DUMMY"
        order.payment_reference = f"DUMMY-{order.id}"
        order.save(update_fields=["status", "payment_method", "payment_reference", "updated_at"])
        # Stock deduction happens via signal
        return Response({"message": "Payment successful. Order is now PAID."}, status=status.HTTP_200_OK)


class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    """
    PATCH /api/v1/orders/<uuid:pk>/status/
    Admin can move through: PAID -> SHIPPED -> DELIVERED (or CANCELLED).
    """
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)

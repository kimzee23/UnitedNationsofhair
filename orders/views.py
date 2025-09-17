
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from orders.models import Order
from orders.permissions import IsOwnerOrAdmin
from orders.serializers import (
    CheckoutSerializer, OrderDetailSerializer, OrderStatusUpdateSerializer
)


class CheckoutView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)
        out = OrderDetailSerializer(order).data
        return Response(out, status=status.HTTP_201_CREATED)


class MyOrdersListView(generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class AdminAllOrdersListView(generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all().order_by("-created_at")


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsOwnerOrAdmin]
    queryset = Order.objects.all()


class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)

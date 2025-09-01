from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from orders.models import Order
from payments.serializers import PaymentInitSerializer, PaymentSerializer
from payments.services import PaymentService

class DummyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if order.status != "PENDING":
            return Response({"detail": f"Order already {order.status}"}, status=400)
        payment = PaymentService.create_dummy_payment(order)
        return Response({"message": "Payment successful", "reference": payment.reference})

class PaymentInitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = PaymentInitSerializer(data=request.data, context={"order": order})
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data["provider"]

        callback_url = request.build_absolute_uri(f"/api/v1/payments/{pk}/callback/")

        if provider == "DUMMY":
            payment = PaymentService.create_dummy_payment(order)
            return Response(PaymentSerializer(payment).data)

        elif provider == "OPAY":
            data = PaymentService.init_opay_payment(order, callback_url)
            return Response(data)

        elif provider == "PAYSTACK":
            data = PaymentService.init_paystack_payment(order, callback_url)
            return Response(data)

        return Response({"detail": "Invalid provider"}, status=400)
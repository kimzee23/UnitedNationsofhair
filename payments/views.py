from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests, hashlib, json

from orders.models import Order, OrderStatus
from payments.serializers import PaymentInitSerializer
from payments.services import PaymentService
from payments.models import PaymentProvider, PaymentStatus


class PaymentInitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.user != request.user:
            return Response({"detail": "Not permitted"}, status=403)
        if order.status != OrderStatus.PENDING:
            return Response({"detail": f"Order already {order.status}"}, status=400)

        serializer = PaymentInitSerializer(data=request.data, context={"order": order})
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data["provider"]

        callback_url = f"{settings.FRONTEND_URL}/payment/callback/"
        if provider == PaymentProvider.PAYSTACK:
            data = PaymentService.init_paystack_payment(order, callback_url)
            return Response(data, status=200)
        elif provider == PaymentProvider.PAYPAL:
            data = PaymentService.init_paypal_payment(
                order,
                return_url=f"{settings.FRONTEND_URL}/payment/paypal/success/",
                cancel_url=f"{settings.FRONTEND_URL}/payment/paypal/cancel/"
            )
            return Response(data, status=200)
        return Response({"detail": "Unsupported provider"}, status=400)


class PaystackWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        signature = request.headers.get("x-paystack-signature")
        body = request.body.decode("utf-8")
        expected_sig = hashlib.sha512(body.encode("utf-8")).hexdigest()
        if signature != expected_sig:
            return Response({"detail": "Invalid signature"}, status=403)

        event = json.loads(body)
        if event.get("event") == "charge.success":
            ref = event["data"].get("reference")
            try:
                order = Order.objects.get(payment_reference=ref)
                if order.status != OrderStatus.PAID:
                    order.status = OrderStatus.PAID
                    order.payment_method = PaymentProvider.PAYSTACK
                    order.payment_reference = ref
                    order.save(update_fields=["status", "payment_method", "payment_reference", "updated_at"])
            except Order.DoesNotExist:
                pass
        return Response({"status": "ok"})


class PayPalExecuteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("paymentId")
        payer_id = request.data.get("PayerID")
        if not payment_id or not payer_id:
            return Response({"detail": "Missing PayPal params"}, status=400)
        try:
            data = PaymentService.execute_paypal_payment(payment_id, payer_id)
            order_id = data["transactions"][0]["description"].split(" ")[1]
            order = Order.objects.get(id=order_id)
            if order.status != OrderStatus.PAID:
                order.status = OrderStatus.PAID
                order.payment_method = PaymentProvider.PAYPAL
                order.payment_reference = payment_id
                order.save(update_fields=["status", "payment_method", "payment_reference", "updated_at"])
            return Response({"message": "PayPal payment successful", "order_id": order.id})
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

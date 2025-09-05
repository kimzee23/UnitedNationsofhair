from payments.serializers import PaymentInitSerializer
import requests, hmac, hashlib, json
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from orders.models import Order, OrderStatus


class PaymentInitView(APIView):
    """
    POST /api/v1/payments/<uuid:pk>/init/
    { "provider": "DUMMY" | "PAYSTACK" }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        # Only the owner can pay
        if order.user != request.user:
            return Response({"detail": "Not permitted."}, status=status.HTTP_403_FORBIDDEN)

        if order.status != OrderStatus.PENDING:
            return Response({"detail": f"Order already {order.status}."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaymentInitSerializer(data=request.data, context={"order": order})
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data["provider"]

        # =Dummy Payment=
        if provider == "DUMMY":
            order.status = OrderStatus.PAID
            order.payment_method = "DUMMY"
            order.payment_reference = f"DUMMY-{order.id}"
            order.save(update_fields=["status", "payment_method", "payment_reference", "updated_at"])

            return Response({
                "message": "Dummy payment successful",
                "order_id": str(order.id),
                "status": order.status
            }, status=status.HTTP_200_OK)

        # =Paystack Payment=
        elif provider == "PAYSTACK":
            url = "https://api.paystack.co/transaction/initialize"
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            data = {
                "email": order.user.email,
                "amount": int(order.total_amount * 100),  # Paystack expects kobo
                "reference": str(order.id),
                "callback_url": f"{settings.FRONTEND_URL}/payment/callback/"
            }

            r = requests.post(url, headers=headers, json=data)
            if r.status_code != 200:
                return Response({"detail": "Paystack error"}, status=status.HTTP_502_BAD_GATEWAY)

            resp = r.json()

            # Save reference + method for later webhook verification
            order.payment_reference = resp["data"]["reference"]
            order.payment_method = "PAYSTACK"
            order.save(update_fields=["payment_reference", "payment_method", "updated_at"])

            return Response({
                "authorization_url": resp["data"]["authorization_url"],
                "access_code": resp["data"]["access_code"],
                "reference": resp["data"]["reference"]
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Unsupported provider"}, status=status.HTTP_400_BAD_REQUEST)

class PaymentVerifyView(APIView):
    """
    GET /api/v1/payments/<uuid:pk>/verify/
    Verifies the order with provider API.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        # Only the owner or staff can verify
        if order.user != request.user and not request.user.is_staff:
            return Response({"detail": "Not permitted."}, status=status.HTTP_403_FORBIDDEN)

        if not order.payment_reference:
            return Response({"detail": "No payment reference found."}, status=status.HTTP_400_BAD_REQUEST)

        if order.payment_method == "PAYSTACK":
            url = f"https://api.paystack.co/transaction/verify/{order.payment_reference}"
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            r = requests.get(url, headers=headers)

            if r.status_code != 200:
                return Response(
                    {"detail": "Error contacting Paystack", "raw": r.text},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            resp = r.json()
            data = resp.get("data", {})

            if data.get("status") == "success":
                if order.status != OrderStatus.PAID:  # prevent double updates
                    order.status = OrderStatus.PAID
                    order.payment_method = "PAYSTACK"  # ensure consistency
                    order.save(update_fields=["status", "payment_method", "updated_at"])

                return Response({
                    "message": "Payment verified successfully",
                    "order_id": str(order.id),
                    "reference": order.payment_reference,
                    "status": order.status
                })

            return Response({"detail": "Payment not verified", "raw": data}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Unsupported payment method"}, status=status.HTTP_400_BAD_REQUEST)


class PaystackWebhookView(APIView):
    """Handle Paystack webhook events"""
    permission_classes = [AllowAny]

    def post(self, request):
        signature = request.headers.get("x-paystack-signature")
        body = request.body.decode("utf-8")

        # Validate signature (Paystack signs with SHA512 hash of body)
        expected_sig = hashlib.sha512(body.encode("utf-8")).hexdigest()
        if signature != expected_sig:
            return Response({"detail": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)

        event = json.loads(body)
        event_name = event.get("event")
        data = event.get("data", {})

        if event_name == "charge.success":
            ref = data.get("reference")
            if not ref:
                return Response({"detail": "No reference in payload"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                order = Order.objects.get(payment_reference=ref)
            except Order.DoesNotExist:
                return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

            if order.status != OrderStatus.PAID:
                order.status = OrderStatus.PAID
                order.payment_method = "PAYSTACK"
                order.save(update_fields=["status", "payment_method", "updated_at"])

        return Response({"status": "ok"})

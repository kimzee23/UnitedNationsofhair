import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from orders.models import Order, OrderStatus
from payments.models import PaymentProvider, Payment


@pytest.mark.django_db
class TestPaymentsAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_init_paystack_payment(self, user, order_factory, settings, requests_mock):
        """Customer can initialize Paystack payment"""
        settings.PAYSTACK_SECRET_KEY = "test_key"
        order = order_factory(user=user, status=OrderStatus.PENDING)

        # Mock Paystack API
        requests_mock.post(
            "https://api.paystack.co/transaction/initialize",
            json={
                "status": True,
                "message": "Authorization URL created",
                "data": {
                    "authorization_url": "https://paystack.com/pay/abc123",
                    "access_code": "xyz789",
                    "reference": "ref123"
                }
            },
            status_code=200,
        )

        self.client.force_authenticate(user=user)
        url = reverse("payment-init", args=[order.id])
        res = self.client.post(url, {"provider": PaymentProvider.PAYSTACK}, format="json")

        assert res.status_code == status.HTTP_200_OK
        assert "authorization_url" in res.data["data"]
        payment = Payment.objects.get(order=order)
        assert payment.provider == PaymentProvider.PAYSTACK
        assert payment.status == "PENDING"

    def test_paystack_webhook_marks_order_paid(self, order_factory, client):
        """Paystack webhook updates order to PAID"""
        order = order_factory(status=OrderStatus.PENDING, payment_reference="ref123")

        body = json.dumps({
            "event": "charge.success",
            "data": {"reference": "ref123"}
        })
        sig = __import__("hashlib").sha512(body.encode("utf-8")).hexdigest()

        url = reverse("paystack-webhook")
        res = client.post(url, data=body, content_type="application/json", **{"HTTP_X_PAYSTACK_SIGNATURE": sig})

        order.refresh_from_db()
        assert res.status_code == 200
        assert order.status == OrderStatus.PAID
        assert order.payment_method == PaymentProvider.PAYSTACK

    def test_init_paypal_payment(self, user, order_factory, mocker, settings):
        """Customer can initialize PayPal payment"""
        settings.PAYPAL_CLIENT_ID = "dummy"
        settings.PAYPAL_SECRET = "dummy"
        settings.PAYPAL_LIVE = False
        settings.PAYPAL_CURRENCY = "USD"

        order = order_factory(user=user, status=OrderStatus.PENDING)

        # Mock PayPal SDK Payment.create
        fake_payment = mocker.Mock()
        fake_payment.id = "PAY-123"
        fake_payment.to_dict.return_value = {"id": "PAY-123", "state": "created"}
        fake_payment.create.return_value = True
        mocker.patch("paypalrestsdk.Payment", return_value=fake_payment)

        self.client.force_authenticate(user=user)
        url = reverse("payment-init", args=[order.id])
        res = self.client.post(url, {"provider": PaymentProvider.PAYPAL}, format="json")

        assert res.status_code == status.HTTP_200_OK
        assert res.data["id"] == "PAY-123"
        payment = Payment.objects.get(order=order)
        assert payment.provider == PaymentProvider.PAYPAL
        assert payment.status == "PENDING"

    def test_execute_paypal_payment_marks_order_paid(self, user, order_factory, mocker, settings):
        """Executing PayPal payment updates order to PAID"""
        settings.PAYPAL_CLIENT_ID = "dummy"
        settings.PAYPAL_SECRET = "dummy"
        settings.PAYPAL_LIVE = False
        settings.PAYPAL_CURRENCY = "USD"

        order = order_factory(user=user, status=OrderStatus.PENDING)

        fake_payment = mocker.Mock()
        fake_payment.execute.return_value = True
        fake_payment.to_dict.return_value = {
            "id": "PAY-123",
            "transactions": [{"description": f"Order {order.id}"}],
        }
        mocker.patch("paypalrestsdk.Payment.find", return_value=fake_payment)

        self.client.force_authenticate(user=user)
        url = reverse("paypal-execute")
        res = self.client.post(url, {"paymentId": "PAY-123", "PayerID": "PAYER-1"}, format="json")

        assert res.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == OrderStatus.PAID
        assert order.payment_method == PaymentProvider.PAYPAL

import uuid

from django.conf import settings
import requests

from orders.models import Order, OrderStatus
from payments.models import Payment, PaymentProvider


class PaymentService:
    @staticmethod
    def create_dummy_payment(order: Order) -> Payment:
        ref = f"DUMMY-{uuid.uuid4().hex[:10]}"
        payment = Payment.objects.create(
            order=order,
            provider=PaymentProvider.DUMMY,
            reference=ref,
            amount=order.total_amount,
            status="SUCCESS"
        )

        order.status = OrderStatus.PAID
        order.payment_method = PaymentProvider.DUMMY
        order.payment_reference = ref
        order.save(update_fields=["status", "payment_method", "payment_reference", "updated_at"])
        return payment

    @staticmethod
    def init_opay_payment(order: Order, callback_url: str) -> dict:
        """
        Initialize payment with Opay.
        Docs: https://documentation.opayweb.com/doc/offline/pos-api.html
        """
        url = settings.OPAY_API_URL + "/api/v1/international/cashier/create"  # check docs
        headers = {
            "Authorization": f"Bearer {settings.OPAY_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        ref = f"OPAY-{uuid.uuid4().hex[:12]}"
        payload = {
            "reference": ref,
            "amount": str(order.total_amount),
            "currency": "NGN",
            "callbackUrl": callback_url,
            "country": "NG",
            "payType": "WEB"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # Save as pending
        Payment.objects.create(
            order=order,
            provider=PaymentProvider.OPAY,
            reference=ref,
            amount=order.total_amount,
            status="PENDING"
        )
        return data

    @staticmethod
    def init_paystack_payment(order: Order, callback_url: str) -> dict:
        """
        Initialize payment with Paystack.
        Docs: https://paystack.com/docs/api/transaction/
        """
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        ref = f"PAYSTACK-{uuid.uuid4().hex[:12]}"
        payload = {
            "reference": ref,
            "amount": int(order.total_amount * 100),  # Paystack expects kobo
            "email": order.user.email,
            "callback_url": callback_url,
            "currency": "NGN"
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # Save as pending
        Payment.objects.create(
            order=order,
            provider=PaymentProvider.PAYSTACK,
            reference=ref,
            amount=order.total_amount,
            status="PENDING"
        )
        return data
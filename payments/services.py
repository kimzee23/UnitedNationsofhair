import uuid
import requests
import paypalrestsdk
from django.conf import settings
from payments.models import Payment, PaymentProvider, PaymentStatus


class PaymentService:
    @staticmethod
    def init_paystack_payment(order, callback_url: str):
        url = "https://api.paystack.co/transaction/initialize"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        ref = f"PAYSTACK-{uuid.uuid4().hex[:12]}"
        payload = {
            "reference": ref,
            "amount": int(order.total_amount * 100),
            "email": order.user.email,
            "callback_url": callback_url,
            "currency": "NGN",
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        Payment.objects.create(
            order=order,
            provider=PaymentProvider.PAYSTACK,
            reference=ref,
            amount=order.total_amount,
            status=PaymentStatus.PENDING,
            metadata=data,
        )
        return data

    @staticmethod
    def init_paypal_payment(order, return_url: str, cancel_url: str):
        paypalrestsdk.configure({
            "mode": "live" if settings.PAYPAL_LIVE else "sandbox",
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_SECRET,
        })
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {"return_url": return_url, "cancel_url": cancel_url},
            "transactions": [{
                "amount": {"total": str(order.total_amount), "currency": settings.PAYPAL_CURRENCY},
                "description": f"Order {order.id}",
            }],
        })
        if not payment.create():
            raise Exception(payment.error)
        Payment.objects.create(
            order=order,
            provider=PaymentProvider.PAYPAL,
            reference=payment.id,
            amount=order.total_amount,
            status=PaymentStatus.PENDING,
            metadata=payment.to_dict(),
        )
        return payment.to_dict()

    @staticmethod
    def execute_paypal_payment(payment_id: str, payer_id: str):
        paypalrestsdk.configure({
            "mode": "live" if settings.PAYPAL_LIVE else "sandbox",
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_SECRET,
        })
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            return payment.to_dict()
        raise Exception(payment.error)


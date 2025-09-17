# payments/urls.py
from django.urls import path
from .views import (
    PaymentInitView,
    PaystackWebhookView,
    PayPalExecuteView,
)

urlpatterns = [
    path("<uuid:pk>/init/", PaymentInitView.as_view(), name="payment-init"),

    path("paystack/webhook/", PaystackWebhookView.as_view(), name="paystack-webhook"),

    path("paypal/execute/", PayPalExecuteView.as_view(), name="paypal-execute"),
]

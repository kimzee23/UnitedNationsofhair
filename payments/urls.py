from django.urls import path
from payments.views import PaymentInitView, PaystackWebhookView, PaymentVerifyView

urlpatterns = [

    path("<uuid:pk>/init/", PaymentInitView.as_view(), name="payment-init"),

    # # Verify payment manually (customer returns from gateway)
    path("<uuid:pk>/verify/", PaymentVerifyView.as_view(), name="payment-verify"),
    path("webhook/paystack/", PaystackWebhookView.as_view(), name="paystack-webhook"),

]

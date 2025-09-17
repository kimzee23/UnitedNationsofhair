from rest_framework import serializers
from .models import Payment, PaymentProvider


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["id", "reference", "amount", "status", "created_at", "updated_at"]


class PaymentInitSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=PaymentProvider.choices)

    def validate(self, attrs):
        order = self.context["order"]
        if order.status != "PENDING":
            raise serializers.ValidationError(f"Order already {order.status}")
        return attrs

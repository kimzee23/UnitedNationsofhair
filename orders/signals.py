from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order, OrderStatus


@receiver (post_save, sender=Order)
def deduct_stock_on_payment(sender, instance, created, **kwargs):
    if not created and instance.status == OrderStatus.PAID and not instance.stock_deducted:
        for item in instance.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save(update_fields=['stock'])
        instance.stock_deducted = True
        instance.save(update_fields=['stock_deducted'])
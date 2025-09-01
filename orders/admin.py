from django.contrib import admin

from orders.models import OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "unit_price", "quantity","subtotal")
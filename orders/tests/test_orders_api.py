from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from users.models import User
from products.models import Product, Brand, Category
from cart.models import CartItem
from orders.models import Order, OrderStatus


class OrdersAPITestCase(APITestCase):
    def setUp(self):
        self.client : APIClient = self.client

        # Vendor
        self.vendor = User.objects.create_user(
            username="vendor1", email="vendor@example.com",
            password="pass123", role="VENDOR"
        )
        self.brand = Brand.objects.create(name="TestBrand", owner=self.vendor)
        self.category = Category.objects.create(name="Shampoo", slug="shampoo")

        # Customer
        self.customer = (User.objects.create_user
            (
            username="customer1", email="cust@example.com",
            password="pass123", role="CUSTOMER"
        ))

        # Product
        self.product = Product.objects.create(
            name="Test Shampoo",
            price=10.00,
            stock=100,
            brand=self.brand,
            category=self.category,
            is_verified=True
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_checkout_and_pay_order(self):
        """Customer can check out cart and pay dummy"""
        CartItem.objects.create(user=self.customer, product=self.product, quantity=2)
        self.authenticate(self.customer)

        checkout_url = reverse("order-checkout")
        payload = {
            "shipping_full_name": "John Doe",
            "shipping_phone": "080456789",
            "shipping_address_line1": "123 Street",
            "shipping_address_line2": "",
            "shipping_city": "Lagos",
            "shipping_state": "Lagos",
            "shipping_postal_code": "100001",
            "shipping_country": "NG"
        }

        # Checkout
        res = self.client.post(checkout_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.data)
        order_id = res.data["id"]
        self.assertEqual(res.data["status"], OrderStatus.PENDING)
        self.assertEqual(float(res.data["total_amount"]), 20.00)

        # Pay
        pay_url = reverse("order-pay", args=[order_id])
        res2 = self.client.patch(pay_url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK, res2.data)
        self.assertIn("Payment successful", res2.data["message"])

        order = Order.objects.get(id=order_id)
        self.assertEqual(order.status, OrderStatus.PAID)

    def test_admin_can_update_status(self):
        """Only admin can move orders through statuses"""
        order = Order.objects.create(
            user=self.customer,
            total_amount=50,
            shipping_full_name="Jane Doe",
            shipping_address_line1="456 Street",
            shipping_city="Abuja",
            shipping_postal_code="900001",
            shipping_country="NG"
        )
        url = reverse("order-status-update", args=[order.id])

        # Vendor (non-admin) should fail
        self.authenticate(self.vendor)
        res = self.client.patch(url, {"status": OrderStatus.SHIPPED})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Make vendor admin
        self.vendor.is_staff = True
        self.vendor.save()
        self.authenticate(self.vendor)
        res2 = self.client.patch(url, {"status": OrderStatus.SHIPPED})
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["status"], OrderStatus.SHIPPED)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from cart.models import CartItem
from users.models import User
from products.models import Product, Brand, Category


class CartAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="cartapi@gmail.com",
            username="cartapi",
            password="testpass123"
        )

        # Authenticate with JWT
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.brand = Brand.objects.create(name="Brand API", owner=self.user)
        self.category = Category.objects.create(name="Category API")
        self.product = Product.objects.create(
            name="Conditioner",
            price=12.00,
            brand=self.brand,
            category=self.category
        )
        self.list_url = reverse("cart-list-create")

    def test_add_cart_item(self):
        response = self.client.post(self.list_url, {"product": self.product.id, "quantity": 3}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 3)

    def test_list_cart_items(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

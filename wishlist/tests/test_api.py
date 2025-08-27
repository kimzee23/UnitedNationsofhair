from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from wishlist.models import WishlistItem
from users.models import User
from products.models import Product, Brand, Category


class WishlistAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="wishlistapi@gmail.com",
            username="wishlistapi",
            password="testpass123"
        )

        # Get JWT tokens
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.brand = Brand.objects.create(name="Wishlist Brand", owner=self.user)
        self.category = Category.objects.create(name="Wishlist Category")
        self.product = Product.objects.create(
            name="Shampoo",
            price=15.00,
            brand=self.brand,
            category=self.category
        )

        self.list_url = reverse("wishlist-list-create")

    def test_add_wishlist_item(self):
        response = self.client.post(self.list_url, {"product": self.product.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishlistItem.objects.count(), 1)
        self.assertEqual(str(WishlistItem.objects.first()), "wishlistapi - Shampoo")

    def test_list_wishlist_items(self):
        WishlistItem.objects.create(user=self.user, product=self.product)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

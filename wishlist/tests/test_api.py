from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from products.models import Product, Brand, Category
from wishlist.models import WishlistItem

class WishlistAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="wishapi@gmail.com", username="wishapi", password="testpass123"
        )
        self.client.login(username="wishapi", password="testpass123")

        self.brand = Brand.objects.create(name="Brand API", owner=self.user)
        self.category = Category.objects.create(name="Category API")
        self.product = Product.objects.create(
            name="Hair Cream", price=18.00, brand=self.brand, category=self.category
        )
        self.list_url = reverse("wishlist-list-create")

    def test_add_wishlist_item(self):
        response = self.client.post(self.list_url, {"product": self.product.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishlistItem.objects.count(), 1)

    def test_list_wishlist_items(self):
        WishlistItem.objects.create(user=self.user, product=self.product)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

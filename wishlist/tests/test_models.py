from django.test import TestCase
from users.models import User
from products.models import Product, Brand, Category
from wishlist.models import WishlistItem

class WishlistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="wishuser@gmail.com", username="wishuser", password="testpass123"
        )
        self.brand = Brand.objects.create(name="Test Brand", owner=self.user)
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Shampoo", price=10.00, brand=self.brand, category=self.category
        )

    def test_add_to_wishlist(self):
        wishlist_item = WishlistItem.objects.create(user=self.user, product=self.product)
        self.assertEqual(str(wishlist_item), "wishuser - Shampoo")
        self.assertEqual(wishlist_item.user, self.user)
        self.assertEqual(wishlist_item.product, self.product)

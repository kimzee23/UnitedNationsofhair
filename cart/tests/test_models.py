from django.test import TestCase

from cart.models import CartItem
from products.models import Brand, Category, Product
from users.models import User


class CartModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="cartuser@gmail.com",
            username="cartuser",
            password="1234pass",
        )
        self.brand = Brand.objects.create(name="Test Brand", owner=self.user)
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="hair oil", price= 18.00, brand=self.brand, category=self.category
        )
    def test_add_to_cart(self):
        cart_item = CartItem.objects.create(
            user=self.user, product=self.product, quantity=1
        )
        self.assertEqual(str(cart_item), "cartuser - Hair oil x 2")
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.user, self.user)
        self.assertEqual(cart_item.product, self.product)
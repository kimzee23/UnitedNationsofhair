from django.test import TestCase
from users.models import User
from products.models import Brand, Category, Product


class ProductModelTests(TestCase):
    def setUp(self):
        # Create a vendor user
        self.vendor = User.objects.create_user(
            email="vendorOne@gmail.com",
            username="vendorOne",
            phone="1234567890",
            password="vendorpass",
            role=User.Role.VENDOR,
        )

        # Create brand linked to vendor
        self.brand = Brand.objects.create(
            name="Test Brand",
            description="Best beauty products",
            website="https://testbrand.com",
            country="Nigeria",
            owner=self.vendor,
        )

        # Create category
        self.category = Category.objects.create(
            name="Hair Care",
            slug="hair-care"
        )

    def test_product_creation(self):
        product = Product.objects.create(
            name="Moisturizing Shampoo",
            price=19.99,
            stock=50,
            affiliate_url="https://affiliate.com/shampoo",
            image_url="https://images.com/shampoo.jpg",
            brand=self.brand,
            category=self.category,
        )

        # Assertions
        self.assertEqual(product.name, "Moisturizing Shampoo")
        self.assertEqual(product.price, 19.99)
        self.assertEqual(product.stock, 50)
        self.assertEqual(product.brand.name, "Test Brand")
        self.assertEqual(product.category.name, "Hair Care")
        self.assertEqual(product.brand.owner.email, "vendorOne@gmail.com")  # vendor via brand

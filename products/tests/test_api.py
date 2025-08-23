from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient

from products.models import Brand, Category
from users.models import User


class TestProductAPI(APITestCase):
    def setUp(self):
        self.client: APIClient = self.client
        self.user = User.objects.create_user(
            username="vendorOne",
            email="vendorOne@gmail.com",
            password="vendor1234",
            role=User.Role.VENDOR,
        )
        self.client.force_authenticate(user=self.user)

        self.brand = Brand.objects.create(
            name="brandOne",
            description="A new brand",
            website="https://www.brand.com",
            country="Nigeria",
            owner=self.user,
        )

        self.category = Category.objects.create(
            name="Hair care",
            slug="hair-care",
        )

        self.test_image = SimpleUploadedFile(
            name="test_image.png",
            content=b"test_image-content",
            content_type="image/jpeg",
        )

        self.product_data = {
            "name": "shampoo",
            "price": "100.9",
            "stock": 10,
            "brand_id": str(self.brand.id),
            "category_id": str(self.category.id),
            "image": self.test_image,
        }

    def test_product_creation(self):
        self.assertEqual(self.brand.name, "brandOne")
        self.assertEqual(self.category.slug, "hair-care")

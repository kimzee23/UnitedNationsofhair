from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Brand, Category, Product
from users.models import User
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class TestProductDiscoveryAPI(APITestCase):
    def setUp(self):
        # Create a vendor user and authenticate
        self.user = User.objects.create_user(
            username="vendorTwo",
            email="vendorTwo@gmail.com",
            password="vendor1234",
            role=User.Role.VENDOR,
        )
        self.client.force_authenticate(user=self.user)

        # Create brand and category
        self.brand = Brand.objects.create(
            name="brandTwo",
            description="Another brand",
            website="https://www.brandtwo.com",
            country="Nigeria",
            owner=self.user,
        )
        self.category = Category.objects.create(name="Hair care", slug="hair-care")

        # Helper to create image
        def get_test_image():
            file = BytesIO()
            image = Image.new("RGB", (100, 100), color="blue")
            image.save(file, "JPEG")
            file.seek(0)
            return SimpleUploadedFile("test_image.jpg", file.read(), content_type="image/jpeg")

        # Create verified products
        self.products = []
        for i in range(6):
            product = Product.objects.create(
                name=f"Product {i+1}",
                price=50 + i,
                stock=5 + i,
                brand=self.brand,
                category=self.category,
                image=get_test_image(),
                is_verified=True,
            )
            self.products.append(product)

    def test_related_products(self):
        # Pick the first product
        product = self.products[0]
        url = reverse("related-products", kwargs={"pk": product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should not include the product itself, max 5 related
        self.assertTrue(all(p["id"] != str(product.id) for p in response.data))
        self.assertLessEqual(len(response.data), 5)

    def test_trending_products(self):
        url = reverse("trending-products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should return up to 5 verified products ordered by newest
        self.assertLessEqual(len(response.data), 5)
        # Check that products are verified
        for p in response.data:
            self.assertTrue(Product.objects.get(id=p["id"]).is_verified)

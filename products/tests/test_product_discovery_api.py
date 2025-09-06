import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Brand, Category, Product
from users.models import User
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class TestProductDiscoveryAPI(APITestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.user = User.objects.create_user(
            username="vendorTwo",
            email="vendorTwo@gmail.com",
            password="vendor1234",
            role=User.Role.VENDOR,
        )
        self.client.force_authenticate(user=self.user)

        self.brand = Brand.objects.create(
            name="brandTwo",
            description="Another brand",
            website="https://www.brandtwo.com",
            country="Nigeria",
            owner=self.user,
        )
        self.category = (
            Category.objects.create(name="Hair care",
                                    slug="hair-care"))

        def get_test_image(save_folder=None):
            file = BytesIO()
            image = Image.new("RGB", (100, 100), color="blue")
            image.save(file, "JPEG")
            file_content = file.getvalue()

            if save_folder:
                os.makedirs(save_folder,exist_ok=True)
                file_path = os.path.join(save_folder, "test_image.jpg")
                with open(file_path, "wb") as f:
                    f.write(file_content)
                print(f"Image save to: {file_path}")
            file.seek(0)
            return SimpleUploadedFile("test_image.jpg", file.read(), content_type="image/jpeg")

        self.products = []
        for item in range(6):
            product = Product.objects.create(
                name=f"Product {item+1}",
                price=50 + item,
                stock=5 + item,
                brand=self.brand,
                category=self.category,
                image=get_test_image(save_folder="images"),
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
        self.assertTrue(all(pro["id"] != str(product.id) for pro in response.data))
        self.assertLessEqual(len(response.data), 5)

    def test_trending_products(self):
        url = reverse("trending-products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should return up to 5 verified products ordered by newest
        self.assertLessEqual(len(response.data), 5)

        for pro in response.data:
            self.assertTrue(Product.objects.get(id=pro["id"]).is_verified)

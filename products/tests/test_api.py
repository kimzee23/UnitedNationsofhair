import os
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from products.models import Brand, Category, Product
from users.models import User
from vendor.models import Vendor


class TestProductAPI(APITestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.user = User.objects.create_user(
            username="vendorOne",
            email="vendorOne@gmail.com",
            password="vendor1234",
            role=User.Role.VENDOR,
        )
        self.vendor_profile = Vendor.objects.create(
            user=self.user,
            business_name="Vendor one",
        )

        self.client.force_authenticate(user=self.user)

        self.brand = Brand.objects.create(
            name="brandOne",
            description="A new brand",
            website="https://www.brand.com",
            country="Nigeria",
            owner=self.vendor_profile,
        )

        self.category = Category.objects.create(
            name="Hair care",
            slug="hair-care",
        )

        def get_test_image(save_folder=None):
            file = BytesIO()
            image = Image.new("RGB", (100, 100), color="red")
            image.save(file, "JPEG")
            file_content = file.getvalue()

            if save_folder:
                os.makedirs(save_folder, exist_ok=True)
                file_path = os.path.join(save_folder, "test_images.jpg")
                with open(file_path, "wb") as f:
                    f.write(file_content)
                    print(f"File saved to {file_path}")

            file.seek(0)
            return SimpleUploadedFile("test_image.jpg", file.read(), content_type="image/jpeg")

        self.test_image = get_test_image(save_folder="images")

        self.product_data = {
            "name": "shampoo",
            "price": "100.9",
            "stock": 10,
            "brand_id": self.brand.id,  # vendor's brand
            "category_id": self.category.id,
            "image": self.test_image,
        }

    def test_product_creation(self):
        url = reverse("product-list-create")
        response = self.client.post(url, self.product_data, format="multipart")
        print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "shampoo")
        self.assertEqual(float(response.data["price"]), 100.9)
        self.assertEqual(response.data["brand"]["id"], self.brand.id)
        self.assertEqual(response.data["category"]["id"], self.category.id)

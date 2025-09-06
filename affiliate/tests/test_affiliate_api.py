import os
from io import BytesIO
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User
from products.models import Product, Brand, Category
from affiliate.models import AffiliateLink, SponsoredListing, AdSlot


def get_test_image_file(save_folder=None):
    file = BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(file, "JPEG")
    file_content = file.getvalue()
    if save_folder:
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, "test_affiliate_image.jpg")
        with open(file_path, "wb") as f:
            f.write(file_content)
        print(f"Image saved to {file_path}")

    file.seek(0)
    return SimpleUploadedFile("test_affiliate_image.jpg", file_content, content_type="image/jpeg")



class AffiliateAPITestCase(APITestCase):

    def setUp(self):
        self.client: APIClient = APIClient()

        self.admin = User.objects.create_user(
            email="admin@example.com", username="admin", password="admin123", role=User.Role.SUPER_ADMIN
        )
        self.vendor = User.objects.create_user(
            email="vendor@example.com", username="vendor", password="vendor123", role=User.Role.VENDOR
        )
        self.influencer = User.objects.create_user(
            email="influencer@example.com", username="influencer", password="influencer123", role=User.Role.INFLUENCER
        )

        self.brand = Brand.objects.create(name="BrandA", description="Desc", owner=self.vendor)
        self.category = Category.objects.create(name="Hair Care", slug="hair-care")


        self.product = Product.objects.create(
            name="Shampoo",
            price=10.0,
            stock=5,
            brand=self.brand,
            category=self.category,
            is_verified=True
        )

        self.client = APIClient()


    def test_create_affiliate_link(self):
        self.client.force_authenticate(user=self.vendor)
        url = reverse("affiliate-link-list-create")
        data = {"product": str(self.product.id), "code": "AFF123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code"], "AFF123")
        self.assertEqual(response.data["user"], str(self.vendor))

    def test_affiliate_link_click_increment(self):
        link = AffiliateLink.objects.create(
            product=self.product,
            user=self.influencer,
            code="AFFCLICK"
        )
        initial_clicks = link.clicks
        link.increment_clicks()
        self.assertEqual(link.clicks, initial_clicks + 1)


    def test_create_sponsored_listing(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("sponsored-listing-list-create")
        start = timezone.now()
        end = timezone.now() + timezone.timedelta(days=10)
        data = {
            "product": str(self.product.id),
            "brand": str(self.brand.id),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "slot_position": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["is_active"])

    def test_create_ad_slot(self):
        self.client.force_authenticate(user=self.vendor)
        url = reverse("ad-slot-list-create")
        start = timezone.now()
        end = timezone.now() + timezone.timedelta(days=5)
        image_file = get_test_image_file(save_folder="images")
        data = {
            "title": "Summer Sale",
            "brand": str(self.brand.id),
            "link": "https://example.com",
            "slot_type": "banner",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "image": image_file
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Summer Sale")
        self.assertTrue(response.data["is_active"])

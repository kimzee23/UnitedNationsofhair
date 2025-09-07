from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from salons.models import Salon, Stylist


class SalonAPITestCase(APITestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.admin = User.objects.create_user(
            email="admin@example.com",
            username="admin",
            password="admin123",
            role=User.Role.SUPER_ADMIN
        )
        self.vendor = User.objects.create_user(
            email="vendor@example.com",
            username="vendor",
            password="vendor123",
            role=User.Role.VENDOR
        )
        self.salon = Salon.objects.create(
            name="Glamour Hair",
            owner=self.vendor,
            phone="08012345678",
            website="https://glamourhair.com",
            address="123 Main Street",
            city="Lagos",
            country="Nigeria"
        )

    def test_create_salon(self):
        self.client.force_authenticate(user=self.vendor)
        url = reverse("salon-list-create")
        data = {
            "name": "New Salon",
            "phone": "08087654321",
            "website": "https://new-salon.com",
            "address": "123 Main Street",
            "city": "Lagos",
            "country": "Nigeria"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Salon")
        self.assertNotIn("is_active", response.data)
        self.assertNotIn("created_at", response.data)
        self.assertNotIn("updated_at", response.data)

    def test_create_stylist(self):
        self.client.force_authenticate(user=self.vendor)
        url = reverse("stylist-list-create")
        data = {
            "salon": str(self.salon.id),
            "user": str(self.vendor.id),
            "specialization": "Hair Coloring",
            "experience_level": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["specialization"], "Hair Coloring")
        self.assertEqual(response.data["salon"], str(self.salon.id))

    def test_list_salon_super_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("salon-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class StylistAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = User.objects.create_user(
            email="vendor@example.com",
            username="vendor",
            password="vendor123",
            role=User.Role.VENDOR
        )
        self.salon = Salon.objects.create(
            name="Glamour Hair",
            owner=self.vendor,
            phone="08012345678",
            website="https://glamourhair.com",
            address="123 Main Street",
            city="Lagos",
            country="Nigeria"
        )
        self.stylist = Stylist.objects.create(
            user=self.vendor,
            salon=self.salon,
            specialization="Hair Coloring",
            experience_level=1,
            website="https://stylist-portfolio.com"
        )

    def test_create_stylist(self):
        self.client.force_authenticate(user=self.vendor)
        url = reverse("stylist-list-create")
        data = {
            "user": str(self.vendor.id),
            "salon": str(self.salon.id),
            "specialization": "Hair Styling",
            "experience_level": 1,
            "website": "https://newstylist.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["specialization"], "Hair Styling")
        self.assertEqual(response.data["salon"], str(self.salon.id))

    def test_list_stylist(self):
        self.client.force_authenticate(user=self.vendor)
        url = reverse("stylist-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

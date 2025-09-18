from uuid import uuid4
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from salons.models import Salon, Stylist, Region


class SalonAPITestCase(APITestCase):
    def setUp(self):
        self.client: APIClient = APIClient()

        # Users
        self.admin = User.objects.create_user(
            email=f"admin_{uuid4()}@example.com",
            username=f"admin_{uuid4()}",
            password="admin123",
            role=User.Role.SUPER_ADMIN
        )
        self.vendor = User.objects.create_user(
            email=f"vendor_{uuid4()}@example.com",
            username=f"vendor_{uuid4()}",
            password="vendor123",
            role=User.Role.VENDOR
        )

        # Region
        self.region = Region.objects.create(
            name="Global",
            country_code="NG",
            currency="NGN",
            language="en"
        )

        # Salon
        self.salon = Salon.objects.create(
            name="Glamour Hair",
            owner=self.vendor,
            phone="08012345678",
            website="https://glamourhair.com",
            address="123 Main Street",
            city="Lagos",
            country="Nigeria",
            region=self.region
        )

    def test_create_salon(self):
        """Vendor should be able to create a new salon"""
        self.client.force_authenticate(user=self.vendor)
        url = reverse("salons-list-create")

        payload = {
            "name": "New Salon",
            "phone": "08087654321",
            "website": "https://new-salon.com",
            "address": "123 Main Street",
            "city": "Lagos",
            "country": "Nigeria",
            "region": "NG"   # ✅ matches SlugRelatedField
        }

        response = self.client.post(url, payload, format="json")
        if response.status_code != status.HTTP_201_CREATED:
            print("Create Salon Error:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Salon")
        self.assertEqual(response.data["region"], "NG")   # ✅ region returned as slug

    def test_list_salon_super_admin(self):
        """Super admin should see all salons"""
        self.client.force_authenticate(user=self.admin)
        url = reverse("salons-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class StylistAPITestCase(APITestCase):
    def setUp(self):
        self.client : APIClient = APIClient()

        self.vendor = User.objects.create_user(
            email=f"vendor_{uuid4()}@example.com",
            username=f"vendor_{uuid4()}",
            password="vendor123",
            role=User.Role.VENDOR
        )

        self.region = Region.objects.create(
            name="Global",
            country_code="NG",
            currency="NGN",
            language="en"
        )
        self.salon = Salon.objects.create(
            name="Glamour Hair",
            owner=self.vendor,
            phone="08012345678",
            website="https://glamourhair.com",
            address="123 Main Street",
            city="Lagos",
            country="Nigeria",
            region=self.region
        )
        self.stylist_user = User.objects.create_user(
            email=f"stylist_{uuid4()}@example.com",
            username=f"stylist_{uuid4()}",
            password="stylist123",
            role=User.Role.VENDOR
        )

        self.stylist = Stylist.objects.create(
            user=self.stylist_user,
            salon=self.salon,
            specialization="Hair Coloring",
            experience_level=1,
            website="https://stylist-portfolio.com"
        )

    def test_create_stylist(self):
        """Vendor should be able to add a stylist to their salon"""
        self.client.force_authenticate(user=self.vendor)

        new_stylist_user = User.objects.create_user(
            email=f"stylist_{uuid4()}@example.com",
            username=f"stylist_{uuid4()}",
            password="stylist123",
            role=User.Role.VENDOR
        )

        url = reverse("stylists-list-create")
        payload = {
            "user": str(new_stylist_user.id),
            "salon": str(self.salon.id),
            "specialization": "Hair Styling",
            "experience_level": 1,
            "website": "https://newstylist.com"
        }
        response = self.client.post(url, payload, format="json")
        if response.status_code != status.HTTP_201_CREATED:
            print("Create Stylist Error:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["specialization"], "Hair Styling")
        self.assertEqual(str(response.data["salon"]), str(self.salon.id))

    def test_list_stylist(self):
        """Vendor should see stylists under their salons"""
        self.client.force_authenticate(user=self.vendor)
        url = reverse("stylists-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

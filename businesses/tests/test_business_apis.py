from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from businesses.models import Business

User = get_user_model()


class BusinessTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password"
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass"
        )

        self.client = APIClient()

        self.business = Business.objects.create(
            name="Test Hair Co",
            email="biz@example.com",
            phone="08012345678",
            address="Lagos",
            owner=self.user
        )

    def test_apply_business(self):
        # Use a new user (self.user already has a business)
        new_user = User.objects.create_user(
            username="newuser",
            email="newuser@example.com",
            password="password"
        )
        self.client.force_authenticate(user=new_user)

        data = {
            "name": "New Hair Biz",
            "email": "newbiz@example.com",
            "phone": "08123456789",
            "address": "Abuja",
            "description": "Hair extension seller"
        }
        response = self.client.post("/api/v1/businesses/apply/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Business.objects.filter(owner=new_user).count(), 1)

    def test_dashboard_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/businesses/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["name"], "New Hair Biz")
        print(response.status_code, response.data)

    def test_admin_approve_business(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/api/v1/businesses/{self.business.id}/approve/",
            {},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.business.refresh_from_db()
        self.assertEqual(self.business.kyc_status, "APPROVED")

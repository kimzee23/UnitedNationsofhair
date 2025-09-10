from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from leads.models import Lead


class LeadAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.lead_data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "1234567890",
            "interest": "Hair Products",
        }

    def test_create_lead(self):
        url = reverse("lead-create")  # make sure your urls.py uses this name
        response = self.client.post(url, self.lead_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(Lead.objects.first().name, "Jane Doe")

    def test_list_leads(self):
        # Create a lead directly
        Lead.objects.create(
            user=self.user,
            name="John Doe",
            email="john@example.com",
            phone="9876543210",
            interest="Wigs",
        )

        url = reverse("lead-list")  # make sure your urls.py uses this name
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John Doe")

    def test_lead_requires_name_and_email(self):
        url = reverse("lead-create")
        invalid_data = {"interest": "Extensions"}
        response = self.client.post(url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("email", response.data)

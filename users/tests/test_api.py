from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class UserAuthAPITests(APITestCase):
    def setUp(self):
        self.client: APIClient = self.client
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.profile_url = reverse("profile")

        self.user_data = {
            "email": "userOne@gmail.com",
            "username": "userOne",
            "phone": "08225026092",
            "password": "1234pass",
        }

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertTrue(User.objects.filter(email="userOne@gmail.com").exists())

    def test_login_and_profile(self):
        self.client.post(self.signup_url, self.user_data, format="json")
        response = self.client.post(
            self.login_url,
            {"username": self.user_data["email"], "password": self.user_data["password"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]

        # Authenticate with access token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        profile_response = self.client.get(self.profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        # Register user
        self.client.post(self.signup_url, self.user_data, format="json")

        # Login to get tokens
        login_response = self.client.post(
            self.login_url,
            {"username": self.user_data["email"], "password": self.user_data["password"]},
            format="json",
        )

        refresh_token = login_response.data["refresh"]
        access_token = login_response.data["access"]

        # Authenticate with access token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(self.logout_url, {"refresh": refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "You have been logged out successfully.")

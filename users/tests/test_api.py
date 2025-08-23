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
        self.assertTrue(User.objects.filter(email = "userOne@gmail.com").exists())
    def test_login_and_profile(self):
        self.client.post(self.signup_url, self.user_data, format="json")
        response = self.client.post(self.login_url, {
            "username": self.user_data["email"],
            "password": self.user_data["password"]
        })
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_302_FOUND])
        user = User.objects.get(email = self.user_data["email"])
        self.client.force_authenticate(user=user)

    def test_logout(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "You have been logged out successfully.")



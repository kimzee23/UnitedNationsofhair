from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAuthAPITests(APITestCase):
    def setUp(self):
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


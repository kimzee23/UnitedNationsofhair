from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from blog.models import BlogArticle


class BlogPermissionTests(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create_user(
            email="admin@tests.com", username="admin", password="pass123", role=User.Role.SUPER_ADMIN
        )
        self.user_influencer = User.objects.create_user(
            email="influencer@tests.com", username="influencer", password="pass123", role=User.Role.INFLUENCER
        )
        self.user_vendor = User.objects.create_user(
            email="vendor@tests.com", username="vendor", password="pass123", role=User.Role.VENDOR
        )
        self.user_customer = User.objects.create_user(
            email="cust@tests.com", username="cust", password="pass123", role=User.Role.CUSTOMER
        )

        self.blog_url = reverse("blog-list-create")

    def test_customer_cannot_create_blog(self):
        self.client.force_authenticate(user=self.user_customer)
        response = self.client.post(self.blog_url, {"title": "Test Blog", "content": "Some content"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_influencer_can_create_blog(self):
        self.client.force_authenticate(user=self.user_influencer)
        response = self.client.post(self.blog_url, {"title": "Test Blog", "content": "Some content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vendor_cannot_create_blog(self):
        self.client.force_authenticate(user=self.user_vendor)
        response = self.client.post(self.blog_url, {"title": "Test Blog", "content": "Some content"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_blog(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.post(self.blog_url, {"title": "Admin Blog", "content": "Admin content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from tutorials.models import Tutorial
from blog.models import BlogArticle


class SearchAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="influencer",
            email="influencer@tests.com",
            password="testpass123",
            role="INFLUENCER",
        )
        # Create tutorial
        Tutorial.objects.create(
            title="Braiding Tutorial",
            description="Learn braiding",
            content="Steps...",
            created_by=self.user,
            is_published=True,
        )
        # Create blog
        BlogArticle.objects.create(
            title="Best Hair Products",
            slug="best-hair-products",
            body="Full blog content",
            author=self.user,
            is_published=True,
        )

    def test_search_returns_results(self):
        url = reverse("search") + "?q=Hair"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Best Hair Products" in r["title"] for r in response.data["blogs"]))

    def test_empty_search_returns_nothing(self):
        url = reverse("search") + "?q=unknownxyz"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blogs"]), 0)
        self.assertEqual(len(response.data["tutorials"]), 0)

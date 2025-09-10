

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from tutorials.models import Tutorial


class TutorialAPITestCase(TestCase):
    def setUp(self):
        self.client : APIClient = APIClient()
        self.influencer = User.objects.create_user(
            username="influencer",
            email="influencer@test.com",
            password="testpass123",
            role="INFLUENCER",
        )
        self.normal_user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="testpass123",
            role="CUSTOMER",
        )
        self.tutorial = Tutorial.objects.create(
            title="Hair Tutorial 1",
            description="How to style afro",
            content="Step by step...",
            created_by=self.influencer,
            is_published=True,
        )

    def test_influencer_can_create_tutorial(self):
        self.client.force_authenticate(user=self.influencer)
        url = reverse("tutorials-list")
        data = {
            "title": "New Tutorial",
            "description": "Desc",
            "content": "Content",
            "is_published": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutorial.objects.count(), 2)

    def test_customer_cannot_create_tutorial(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("tutorials-list")
        data = {
            "title": "Bad Attempt",
            "description": "Desc",
            "content": "Content",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_can_view_published_tutorials(self):
        url = reverse("tutorials-public-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_view_single_tutorial_increases_views(self):
        views_before = self.tutorial.views
        url = reverse("tutorials-public-detail", args=[self.tutorial.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tutorial.refresh_from_db()
        self.assertEqual(self.tutorial.views, views_before + 1)

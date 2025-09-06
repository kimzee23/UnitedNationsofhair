from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from engagement.models import Comment, Like, Follow
from products.models import Product, Brand, Category
from blog.models import BlogArticle

User = get_user_model()


class EngagementTestCase(TestCase):
    def setUp(self):
        self.client : APIClient = APIClient()

        # Create main user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            role="CUSTOMER"
        )

        # Create another user to follow
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123",
            role="CUSTOMER"
        )

        # Force authenticate to avoid 401
        self.client.force_authenticate(user=self.user)

        # Create vendor, brand, category, product
        self.vendor = User.objects.create_user(
            username="vendoruser",
            email="vendor@example.com",
            password="password123",
            role="VENDOR"
        )

        self.brand = Brand.objects.create(
            name="Test Brand",
            description="Test Brand Description",
            owner=self.vendor
        )

        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )

        self.product = Product.objects.create(
            name="Test Product",
            price=10.00,
            stock=5,
            brand=self.brand,
            category=self.category
        )


        self.blog = BlogArticle.objects.create(
            title="Best hair cream",
            body="This is a test blog content.",
            author=self.user
        )

    # ---------- COMMENTS ----------
    def test_create_comment(self):
        data = {"content": "Nice blog!"}
        response = self.client.post(
            f"/api/v1/engagement/blog/{self.blog.id}/comments/",
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, "Nice blog!")

    # ---------- LIKES ----------
    def test_toggle_like(self):

        response1 = self.client.post(
            f"/api/v1/engagement/product/{self.product.id}/like/"
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

        # Unlike the product
        response2 = self.client.post(
            f"/api/v1/engagement/product/{self.product.id}/like/"
        )
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 0)

    # ---------- FOLLOWS ----------
    def test_toggle_follow(self):

        response1 = self.client.post(
            f"/api/v1/engagement/follow/{self.other_user.id}/"
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)

        # Unfollow
        response2 = self.client.post(
            f"/api/v1/engagement/follow/{self.other_user.id}/"
        )
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 0)

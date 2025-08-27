from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from products.models import Product, Brand, Category


class ReviewAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="userReview@gmail.com",
            username="userReview",
            password="1234pass",
        )

        # Create brand and category (because Product requires them)
        self.brand = Brand.objects.create(name="Test Brand", owner=self.user)
        self.category = Category.objects.create(name="Test Category")

        # Create product
        self.product = Product.objects.create(
            name="hair cleaner",
            price=20.00,
            brand=self.brand,
            category=self.category,
        )

        login_url = reverse("login")
        login_response = self.client.post(
            login_url,
            {"username": self.user.email, "password": "1234pass"},
            format="json",
        )
        print("DEBUG login response:", login_response.data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        self.list_url = reverse("review-list-create")

    def test_create_review(self):
        data = {"rating": 5, "comment": "Excellent", "product": str(self.product.id)}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.review_set.count(), 1)


    def test_list_review(self):
        from reviews.models import Review
        Review.objects.create(user=self.user, product=self.product, rating=4, comment="Good")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

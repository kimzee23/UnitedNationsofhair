from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from products.models import Product
from reviews.models import Review
from users.models import User


class ReviewAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="userReview@gmail.com",
            username="userReview",
            password="1234pass",
        )
        self.product = Product.objects.create(
            name="hair cleaner",
            description="cleaner hair 2 times faster",
            price=20.00,
        )
        self.client.login(username="userReview", password="1234pass")
        self.list_url = reverse("review-list-create")

    def test_create_review(self):
        data = {"rating" : 5 , "comment" : "Excellent", "product" : self.product.id}
        response = self.client.post(self.list_url,  format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_list_review(self):
        Review.objects.create(user=self.user, product=self.product, rating=4, comment="Excellent")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
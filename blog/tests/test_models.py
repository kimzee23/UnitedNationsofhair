from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from users.models import User
from blog.models import BlogArticle


class BlogArticleModelTests(TestCase):
    def setUp(self):
        self.influencer = User.objects.create_user(
            email="influencer@test.com",
            username="influencer1",
            phone="1234567890",
            password="pass1234",
            role=User.Role.INFLUENCER
        )
        self.super_admin = User.objects.create_user(
            email="admin@test.com",
            username="admin1",
            phone="1234567891",
            password="pass1234",
            role=User.Role.SUPER_ADMIN
        )
        self.customer = User.objects.create_user(
            email="customer@test.com",
            username="customer1",
            phone="1234567892",
            password="pass1234",
            role=User.Role.CUSTOMER
        )

    def test_influencer_can_create_blog(self):
        blog = BlogArticle.objects.create(
            title="Influencer Blog",
            slug="influencer-blog",
            body="This is a blog by influencer.",
            author=self.influencer
        )
        self.assertEqual(blog.author, self.influencer)

    def test_superadmin_can_create_blog(self):
        blog = BlogArticle.objects.create(
            title="Admin Blog",
            slug="admin-blog",
            body="This is a blog by super admin.",
            author=self.super_admin
        )
        self.assertEqual(blog.author, self.super_admin)

    def test_customer_cannot_create_blog(self):
        blog = BlogArticle(
            title="Customer Blog",
            slug="customer-blog",
            body="This should not be allowed.",
            author=self.customer
        )

        with self.assertRaises(ValidationError):
            blog.full_clean()   # run validation
            blog.save()

class BlogArticleAPITests(APITestCase):
    def setUp(self):
        self.client: APIClient = self.client
        self.user = User.objects.create_user(
                username="influencerOne",
                email="influencerOne@gmail.com",
                password="1234pass",
                role=User.Role.INFLUENCER
            )
        self.client.force_authenticate(user=self.user)

        self.blog_data = {
                "title": "Hair Growth Tips",
                "slug": "hair-growth-tips",
                "body": "This blog is about natural hair growth tips.",
                "tags": ["hair", "natural", "growth"],
            }
        from django.urls import reverse
        self.list_url = reverse("blog-list-create")

    def test_customer_cannot_create_blog(self):
            customer = User.objects.create_user(
                email="cust@test.com",
                username="cust",
                password="pass123",
                role=User.Role.CUSTOMER
            )
            self.client.force_authenticate(user=customer)
            response = self.client.post(self.list_url, data=self.blog_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
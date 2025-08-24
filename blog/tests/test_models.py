from django.test import TestCase
from django.core.exceptions import ValidationError
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
        # Since limit_choices_to only affects the admin/ORM UI,
        # make i  enforce check manually here
        if blog.author.role not in [User.Role.INFLUENCER, User.Role.SUPER_ADMIN]:
            with self.assertRaises(ValidationError):
                blog.full_clean()   # run validation before saving

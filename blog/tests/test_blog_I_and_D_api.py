from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User
from blog.models import BlogArticle


class BlogArticleAPITestCase(APITestCase):

    def setUp(self):
        self.client : APIClient = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            username="adminuser",
            password="password123",
            role=User.Role.SUPER_ADMIN
        )
        self.influencer_user = User.objects.create_user(
            email="influencer@example.com",
            username="influencer",
            password="password123",
            role=User.Role.INFLUENCER
        )
        self.normal_user = User.objects.create_user(
            email="customer@example.com",
            username="normaluser",
            password="password123",
            role=User.Role.CUSTOMER
        )


        self.published_article = BlogArticle.objects.create(
            title="Published Blog",
            slug="published-blog",
            body="This is a published article.",
            author=self.influencer_user,
            is_published=True,
        )

        self.unpublished_article = BlogArticle.objects.create(
            title="Draft Blog",
            slug="draft-blog",
            body="This is a draft article.",
            author=self.influencer_user,
            is_published=False,
        )

        self.private_list_url = reverse("blog-list-create")
        self.private_detail_url_published = reverse("blog-detail", args=[self.published_article.id])
        self.private_detail_url_unpublished = reverse("blog-detail", args=[self.unpublished_article.id])


        self.public_list_url = reverse("public-blog-list")
        self.public_detail_url_published = reverse("public-blog-detail", args=[self.published_article.slug])
        self.public_detail_url_unpublished = reverse("public-blog-detail", args=[self.unpublished_article.slug])


    def test_public_can_see_only_published_articles(self):
        response = self.client.get(self.public_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [article["title"] for article in response.data]
        self.assertIn("Published Blog", titles)
        self.assertNotIn("Draft Blog", titles)

    def test_public_can_view_published_article_detail(self):
        response = self.client.get(self.public_detail_url_published)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Published Blog")

    def test_public_cannot_view_unpublished_article_detail(self):
        response = self.client.get(self.public_detail_url_unpublished)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # -----------------------
    # Private API tests


    def test_admin_can_see_all_articles(self):
        self.client.login(email="admin@example.com", password="password123")
        response = self.client.get(self.private_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [article["title"] for article in response.data]
        self.assertIn("Published Blog", titles)
        self.assertIn("Draft Blog", titles)

    def test_influencer_can_create_article(self):
        self.client.force_authenticate(user=self.influencer_user)
        data = {
            "title": "New Influencer Post",
            "slug": "new-influencer-post",
            "body": "Some influencer content",
            "is_published": True
        }
        response = self.client.post(self.private_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], self.influencer_user.id)

    def test_customer_cannot_create_article(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {
            "title": "Customer Post",
            "slug": "customer-post",
            "body": "Customers should not be able to post",
            "is_published": True
        }
        response = self.client.post(self.private_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

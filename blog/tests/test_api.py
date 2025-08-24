from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from blog.models import BlogArticle
from users.models import User


class BlogArticleAPITests(APITestCase):
    def setUp(self):
        self.client: APIClient = self.client
        self.user = User.objects.create_user(
            username="influencerOne",
            email="influencerOne@gmail.com",
            password="1234pass",
            role = User.Role.INFLUENCER
        )
        self.client.force_authenticate(user=self.user)

        self.blog_data = {
            "title": "Hair Growth Tips",
            "slug": "hair-growth-tips",
            "body": "This blog is about natural hair growth tips.",
            "tags": ["hair", "natural", "growth"],
        }
        self.list_url = reverse("blog-list-create")

    def test_create_blog_article(self):
        response = self.client.post(self.list_url, data=self.blog_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogArticle.objects.count(), 1)
        self.assertEqual(BlogArticle.objects.first().title, "Hair Growth Tips")

    def test_list_blog_article(self):
        BlogArticle.objects.create(
            title = "Hair Growth Tips",
            slug = "hair-growth-tips",
            body = "This blog is about.",
            author = self.user,
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_blog_article(self):
        blog = BlogArticle.objects.create(
            title="Another Blog",
            slug="another-blog",
            body="Some text here",
            author=self.user,
        )
        url = reverse("blog-detail", args=[blog.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Another Blog")

    def test_update_blog_article(self):
        blog = BlogArticle.objects.create(
            title="Old Title",
            slug="old-title",
            body="Old body",
            author=self.user,
        )
        url = reverse("blog-detail", args=[blog.id])
        response = self.client.patch(url, {"title": "Updated Title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog.refresh_from_db()
        self.assertEqual(blog.title, "Updated Title")

    def test_delete_blog_article(self):
        blog = BlogArticle.objects.create(
            title="Delete Me",
            slug="delete-me",
            body="Text",
            author=self.user,
        )
        url = reverse("blog-detail", args=[blog.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlogArticle.objects.filter(id=blog.id).exists())
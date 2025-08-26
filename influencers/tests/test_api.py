from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from influencers.models import Influencer, InfluencerProduct
from products.models import Product, Brand

from rest_framework_simplejwt.tokens import RefreshToken

class InfluencerAPITestCase(APITestCase):
    def setUp(self):
        self.client: APIClient = self.client

        self.influencer_user = User.objects.create_user(
            username="influencer1",
            email="influencer1@example.com",
            password="password123",
            role="INFLUENCER"
        )
        self.owner_user = User.objects.create_user(
            username="owner1",
            email="owner1@example.com",
            password="password123",
            role="VENDOR"
        )

        # Generate JWT token for the user that should perform API actions
        refresh = RefreshToken.for_user(self.owner_user)
        access_token = str(refresh.access_token)

        # Authenticate client with JWT
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Create brand and product
        self.brand = Brand.objects.create(
            name="Test Brand",
            owner=self.owner_user
        )
        self.product = Product.objects.create(
            name="Test Product",
            brand=self.brand
        )

        # Create influencer
        self.influencer = Influencer.objects.create(
            user=self.influencer_user,
            bio="Test bio",
            followers_count=100
        )

        # Set the URL
        self.influencer_products_url = reverse('influencer-products-list')

    def test_create_influencer_product(self):
        data = {
            "influencer_id": str(self.influencer.id),
            "product_id": str(self.product.id),
            "promote_url": "https://example.com/promo"
        }
        response = self.client.post(self.influencer_products_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InfluencerProduct.objects.count(), 1)
        self.assertEqual(InfluencerProduct.objects.first().promote_url, data["promote_url"])

    def test_prevent_duplicate_influencer_product(self):
        InfluencerProduct.objects.create(influencer=self.influencer, product=self.product)
        data = {
            "influencer_id": str(self.influencer.id),
            "product_id": str(self.product.id)
        }
        response = self.client.post(self.influencer_products_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already promoting", str(response.data))

    def test_list_influencer_products(self):
        InfluencerProduct.objects.create(influencer=self.influencer, product=self.product)
        response = self.client.get(self.influencer_products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_influencer_product(self):
        ip = InfluencerProduct.objects.create(influencer=self.influencer, product=self.product)
        url = reverse('influencer-products-detail', args=[ip.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InfluencerProduct.objects.count(), 0)

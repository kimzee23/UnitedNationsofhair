from django.test import TestCase
from users.models import User
from products.models import Brand, Category, Product
from influencers.models import Influencer, InfluencerProduct


class InfluencerModelTests(TestCase):
    def setUp(self):
        # Create a vendor user + brand + category + product
        self.vendor = User.objects.create_user(
            email="vendor@gmail.com",
            username="vendor",
            phone="1234567890",
            password="vendorpass",
            role=User.Role.VENDOR,
        )

        self.brand = Brand.objects.create(
            name="BeautyBrand",
            owner=self.vendor,
        )

        self.category = Category.objects.create(
            name="Skincare",
            slug="skincare"
        )

        self.product = Product.objects.create(
            name="Face Cream",
            price=29.99,
            stock=100,
            brand=self.brand,
            category=self.category,
        )

        # Create influencer user
        self.influencer_user = User.objects.create_user(
            email="influencer@gmail.com",
            username="influencer",
            phone="0987654321",
            password="influencerpass",
            role=User.Role.INFLUENCER,
        )

        # Link influencer profile to influencer user
        self.influencer = Influencer.objects.create(
            user=self.influencer_user,
            bio="Skin care enthusiast",
            followers_count=5000,
            social_links={"instagram": "https://instagram.com/influencer"}
        )

    def test_influencer_creation(self):
        self.assertEqual(self.influencer.user.email, "influencer@gmail.com")
        self.assertEqual(self.influencer.followers_count, 5000)
        self.assertIn("instagram", self.influencer.social_links)

    def test_influencer_promotes_product(self):
        ip = InfluencerProduct.objects.create(
            influencer=self.influencer,
            product=self.product,
            promote_url="https://promo.link/face-cream"
        )

        self.assertEqual(ip.influencer.user.username, "influencer")
        self.assertEqual(ip.product.name, "Face Cream")
        self.assertEqual(ip.promote_url, "https://promo.link/face-cream")

    def test_influencer_product_unique_constraint(self):
        InfluencerProduct.objects.create(
            influencer=self.influencer,
            product=self.product,
            promote_url="https://promo.link/face-cream"
        )

        with self.assertRaises(Exception):
            InfluencerProduct.objects.create(
                influencer=self.influencer,
                product=self.product,
                promote_url="https://another.link"
            )

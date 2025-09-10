from rest_framework import serializers
from products.models import Product
from blog.models import BlogArticle
from salons.models import Salon, Stylist

class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "thumbnail"]

class BlogSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogArticle
        fields = ["id", "title", "author", "created_at"]

class SalonSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ["id", "name", "location"]

class StylistSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stylist
        fields = ["id", "name", "specialty"]

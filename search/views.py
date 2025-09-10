from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from blog.models import BlogArticle
from salons.models import Salon, Stylist
from .serializers import (
    ProductSearchSerializer,
    BlogSearchSerializer,
    SalonSearchSerializer,
    StylistSearchSerializer,
)


class GlobalSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        results = {}

        if query:
            products = Product.objects.filter(name__icontains=query, is_verified=True)[:5]
            results["products"] = ProductSearchSerializer(products, many=True).data

            blogs = BlogArticle.objects.filter(title__icontains=query, is_published=True)[:5]
            results["blogs"] = BlogSearchSerializer(blogs, many=True).data

            salons = Salon.objects.filter(name__icontains=query)[:5]
            results["salons"] = SalonSearchSerializer(salons, many=True).data

            stylists = Stylist.objects.filter(name__icontains=query)[:5]
            results["stylists"] = StylistSearchSerializer(stylists, many=True).data

        return Response(results)

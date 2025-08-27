from rest_framework import generics
from products.models import Brand, Category, Product
from products.serializers import BrandSerializer, CategorySerializer, ProductSerializer
from users.permissions import IsVendorOrAdmin

class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsVendorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsVendorOrAdmin]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
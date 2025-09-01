from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

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

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


    filterset_fields = {
        "category__id": ["exact"],
        "category__name": ["icontains"],
        "brand__id": ["exact"],
        "brand__name": ["icontains"],
        "price": ["gte", "lte"],
        "stock": ["gte", "lte"],
    }

    search_fields = ["name", "brand__name", "category__name"]

    ordering_fields = ["price", "stock", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.role in ["VENDOR", "SUPER_ADMIN"]):
            return Product.objects.all()
        return Product.objects.filter(is_verified=True)

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

class ProductVerifyView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_verified = True
        product.save()
        return Response({"message": f" {product.name} has been verified."}, status=status.HTTP_200_OK)

@api_view(["GET"])
def related_products(request, pk):
        try:
            product = Product.objects.get(pk=pk, is_verified=True)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        related = Product.objects.filter(
            category=product.category,
            is_verified=True
        ).exclude(id=product.id)[:5]  # limit 5

        serializer = ProductSerializer(related, many=True, context={"request": request})
        return Response(serializer.data)

    # Trending products (mock: most reviewed / later by sales)
@api_view(["GET"])
def trending_products(request):
        trending = Product.objects.filter(is_verified=True).order_by("-created_at")[:5]
        # TODO: later use review count / sales stats
        serializer = ProductSerializer(trending, many=True, context={"request": request})
        return Response(serializer.data)


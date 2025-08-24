from django.urls import path, include

from products.views import BrandListCreateView, CategoryListCreateView, ProductListCreateView, ProductDetailView

urlpatterns = [
    path("users/", include("users.urls")),
    path("brands/", BrandListCreateView.as_view(), name="brand-list-create"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
]

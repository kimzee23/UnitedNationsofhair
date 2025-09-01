from django.urls import path, include

from products.views import BrandListCreateView, CategoryListCreateView, ProductListCreateView, ProductDetailView, \
    ProductVerifyView, related_products, trending_products

urlpatterns = [
    path("users/", include("users.urls")),
    path("brands/", BrandListCreateView.as_view(), name="brand-list-create"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("<uuid:pk>/verify/", ProductVerifyView.as_view(), name="product-verify"),

    path("<uuid:pk>/related/", related_products, name="related-products"),
    path("trending/", trending_products, name="trending-products"),
 ]











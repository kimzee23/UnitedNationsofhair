from django.urls import path, include
from .views import (
    BrandListCreateView,
    CategoryListCreateView,
    ProductListCreateView,
    ProductDetailView,
    ProductVerifyView,
    RelatedProductsView,
    TrendingProductsView, ProductCompareView,
)

urlpatterns = [
    path("users/", include("users.urls")),

    path("brands/", BrandListCreateView.as_view(), name="brand-list-create"),

    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),


    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("<uuid:pk>/verify/", ProductVerifyView.as_view(), name="product-verify"),


    path("<uuid:pk>/related/", RelatedProductsView.as_view(), name="related-products"),
    path("products/trending/", TrendingProductsView.as_view(), name="trending-products"),
    path("compare/", ProductCompareView.as_view(), name="product-compare"),

]







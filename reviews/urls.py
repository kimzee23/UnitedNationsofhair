from django.urls import path
from reviews.views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path("", ReviewListCreateView.as_view(), name="review-list-create"),
    path("<uuid:pk>/", ReviewDetailView.as_view(), name="review-detail"),

]

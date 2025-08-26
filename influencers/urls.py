from django.urls import path, include
from rest_framework.routers import DefaultRouter
from influencers.views import InfluencerViewSet, InfluencerProductViewSet

router = DefaultRouter()
router.register(r'influencers', InfluencerViewSet, basename='influencers')
router.register(r'influencer-products', InfluencerProductViewSet, basename='influencer-products')

urlpatterns = [
    path('', include(router.urls)),
]

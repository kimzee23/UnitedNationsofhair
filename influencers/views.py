from rest_framework import viewsets
from influencers.models import Influencer, InfluencerProduct
from influencers.serializers import InfluencerSerializer, InfluencerProductSerializer
from rest_framework.permissions import IsAuthenticated


class InfluencerViewSet(viewsets.ModelViewSet):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer
    permission_classes = [IsAuthenticated]


class InfluencerProductViewSet(viewsets.ModelViewSet):
    queryset = InfluencerProduct.objects.all()
    serializer_class = InfluencerProductSerializer
    permission_classes = [IsAuthenticated]

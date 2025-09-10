from django.urls import path
from .views import (
    TutorialListCreateView,
    TutorialDetailView,
    PublicTutorialListView,
    PublicTutorialDetailView,
)

urlpatterns = [
    path("tutorials/", TutorialListCreateView.as_view(), name="tutorials-list"),
    path("tutorials/<int:pk>/", TutorialDetailView.as_view(), name="tutorials-detail"),
    path("public/tutorials/", PublicTutorialListView.as_view(), name="tutorials-public-list"),
    path("public/tutorials/<int:pk>/", PublicTutorialDetailView.as_view(), name="tutorials-public-detail"),
]

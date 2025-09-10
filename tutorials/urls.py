from django.urls import path

from tutorials.views import TutorialListCreateView, TutorialDetailView

urlpatterns = [
    path("", TutorialListCreateView.as_view(), name="tutorial-list-create"),
    path("<int:pk>", TutorialDetailView.as_view(), name="tutorial-detail"),
]
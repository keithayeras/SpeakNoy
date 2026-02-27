from django.urls import path
from .views import FlashcardListView, FlashcardDetailView

urlpatterns = [
    path("", FlashcardListView.as_view(), name="cardlist"),
    path("<int:pk>/", FlashcardDetailView.as_view(), name="card"),
]

app_name = 'SpeakNoy'
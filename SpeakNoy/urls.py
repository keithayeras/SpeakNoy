from django.urls import path
from .views import flashcard_list_view, flashcard_detail_view

urlpatterns = [
    path("", flashcard_list_view, name="cardlist"),
    path("<int:pk>/", flashcard_detail_view, name="card"),
]

app_name = 'SpeakNoy'
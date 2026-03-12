from django.urls import path
from .views import flashcard_list_view, flashcard_detail_view, daily_review_view, dialect_review_view

urlpatterns = [
    path("", flashcard_list_view, name="cardlist"),
    path("<int:pk>/", flashcard_detail_view, name="card"),
    path("review/", daily_review_view, name="daily_review"),
    path("review/all/", dialect_review_view, name="dialect_review"),
]

app_name = 'SpeakNoy'
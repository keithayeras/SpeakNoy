from django.urls import path
from .views import *

urlpatterns = [
    path("", flashcard_list_view, name="cardlist"),
    path("<int:pk>/", flashcard_detail_view, name="card"),
    path("review/", daily_review_view, name="daily_review"),
    path("review/all/", dialect_review_view, name="dialect_review"),
    path("addcard/", flashcard_create_view, name="cardcreate"),
    path("removecard/<int:pk>/", flashcard_remove, name="cardremove"),
]

app_name = 'SpeakNoy'
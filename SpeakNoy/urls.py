from django.urls import path
from .views import *

urlpatterns = [
    path("", flashcard_list_view, name="cardlist"),
    path("<int:pk>/", flashcard_detail_view, name="card"),
    path("addcard/", flashcard_create_view, name="cardcreate"),
]

app_name = 'SpeakNoy'
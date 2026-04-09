from django.urls import path
from .views import *

urlpatterns = [
    path("", flashcard_list_view, name="cardlist"),
    path("<int:pk>/", flashcard_detail_view, name="card"),
    path("review/", daily_review_view, name="daily_review"),
    path("review/all/", dialect_review_view, name="dialect_review"),
    path("addcard/", flashcard_create_view, name="cardcreate"),
    path("removecard/<int:pk>/", flashcard_remove, name="cardremove"),
    path('collections/', collection_list_view, name='collection_list'),
    path('collections/new/', collection_create_view, name='collection_create'),
    path('collections/<int:pk>/', collection_detail_view, name='collection_detail'),
    path('<int:pk>/add-to-collection/', collection_add_card, name='add_to_collection'),
]

app_name = 'SpeakNoy'
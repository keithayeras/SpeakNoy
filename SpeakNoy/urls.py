from django.urls import path
from .views import *

urlpatterns = [
    path("", flashcard_list_view, name="cardlist"),
    path("<int:pk>/", flashcard_detail_view, name="card"),
    path("review/", daily_review_view, name="daily_review"),
    path("review/all/", dialect_review_view, name="dialect_review"),
    path("addcard/", flashcard_create_view, name="cardcreate"),
    path("removecard/<int:pk>/", flashcard_remove, name="cardremove"),
    path('collections/', collection_list_view, name='collectionlist'),
    path('collections/<int:pk>/', collection_detail_view, name='collection'),
    path('collections/addcollection/', collection_create_view, name='collectioncreate'),
    path('<int:pk>/add-to-collection/', collection_add_card, name='add_to_collection'),
    path('publicspace/', publicspace_view, name='publicspace'),
    path('<int:pk>/upload-card-to-publicspace', publicspace_upload_card, name='publicspace-upload-card'),
    path('<int:pk>/upload-collection-to-publicspace', publicspace_upload_collection, name='publicspace-upload-collection'),
    path('<int:pk>/remove-card-from-publicspace', publicspace_remove_card, name='publicspace-remove-card'),
    path('<int:pk>/remove-collection-from-publicspace', publicspace_remove_collection, name='publicspace-remove-collection'),
    path('<int:pk>/save-card-from-publicspace', publicspace_save_card, name='publicspace-save-card'),
    path('<int:pk>/save-collection-from-publicspace', publicspace_save_collection, name='publicspace-save-collection'),
]

app_name = 'SpeakNoy'
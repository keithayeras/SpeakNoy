from django.shortcuts import render
from django.views.generic import *
from .models import Flashcard
# Create your views here.

class FlashcardListView(ListView):
    model = Flashcard
    template_name = "flashcard_list.html"
    context_object_name = "flashcard"

class FlashcardDetailView(DetailView):
    model = Flashcard
    template_name = "flashcard_detail.html"
    context_object_name = "flashcard"
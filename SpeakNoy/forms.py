from django import forms
from django.forms import ModelForm
from .models import *

class FlashcardForm(ModelForm):
    class Meta:
        model = Flashcard
        fields = [
            'word',
            'pronunciation',
            'definition',
            'purpose',
            ]
        
class FlashcardCollectionForm(ModelForm):
    class Meta:
        model = FlashcardCollection
        fields = ['name']

class AddToCollectionForm(forms.Form):
    collection = forms.ModelChoiceField(
        queryset=FlashcardCollection.objects.all(),
        label="Choose which collection your card will be in"
    )
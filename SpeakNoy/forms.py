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

class RemoveFromCollectionForm(forms.Form):
    collection = forms.ModelChoiceField(
        queryset=FlashcardCollection.objects.all(),
        label="Choose which collection you would like to remove the card from"
    )

class PublicSpaceForm(ModelForm):
    class Meta:
        model = PublicSpace
        fields = ['name']
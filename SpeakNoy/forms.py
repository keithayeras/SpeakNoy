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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['collection'].queryset = FlashcardCollection.objects.filter(creator=user)

class RemoveFromCollectionForm(forms.Form):
    collection = forms.ModelChoiceField(
        queryset=Flashcard.objects.none(),
        label="Choose which card you would like to remove from this collection"
    )
    
    def __init__(self, *args, **kwargs):
        collection_id = kwargs.pop('collection_id', None)
        super().__init__(*args, **kwargs)
        if collection_id:
            self.fields['collection'].queryset = Flashcard.objects.filter(collections=collection_id)

class PublicSpaceForm(ModelForm):
    class Meta:
        model = PublicSpace
        fields = ['name']
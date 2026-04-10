from django.contrib import admin
from .models import *

class FlashcardAdmin(admin.ModelAdmin):
    model = Flashcard
class FlashcardCollectionAdmin(admin.ModelAdmin):
    model = FlashcardCollection

# Register your models here.
admin.site.register(Flashcard, FlashcardAdmin)
admin.site.register(FlashcardCollection, FlashcardCollectionAdmin)
from django.contrib import admin
from .models import Flashcard

class FlashcardAdmin(admin.ModelAdmin):
    model = Flashcard

# Register your models here.
admin.site.register(Flashcard, FlashcardAdmin)
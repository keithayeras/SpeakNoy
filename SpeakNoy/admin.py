from django.contrib import admin
from .models import *

class FlashcardAdmin(admin.ModelAdmin):
    model = Flashcard
class 

# Register your models here.
admin.site.register(Flashcard, FlashcardAdmin)
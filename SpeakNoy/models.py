from django.db import models

# Create your models here.
class Flashcard(models.Model):
    PURPOSE_CHOICES = [
        ("Noun", "Noun"),
        ("Pronoun", "Pronoun"),
        ("Verb", "Verb"),
        ("Adjective", "Adjective"),
        ("Adverb", "Adverb"),
    ]

    word = models.CharField(max_length=63)
    pronunciation = models.CharField(max_length=63)
    definition = models.TextField()
    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES,
        default="Noun"
    )

    def __str__(self):
        return self.word
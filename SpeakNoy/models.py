from django.db import models

# Create your models here.
class Flashcard(models.Model):
    PURPOSE_CHOICES = [
        ("noun", "Noun"),
        ("pronoun", "Pronoun"),
        ("verb", "Verb"),
        ("adjective", "Adjective"),
        ("adverb", "Adverb"),
    ]

    word = models.CharField(max_length=63)
    pronunciation = models.CharField(max_length=63)
    definition = models.TextField()
    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES,
        default="noun"
    )

    def __str__(self):
        return self.word